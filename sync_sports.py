"""
Sync live sports fixtures from The Odds API.
Run with: python sync_sports.py (from project root)

Supports: Football (Premier League, La Liga, Serie A, Bundesliga),
Basketball (NBA), Tennis, Rugby.
"""
import requests
import os
from datetime import datetime
from app.extensions import db
from app.models.sports import SportsEvent, SportsMarket, SportsSelection

# The Odds API sport codes
SPORTS_TO_SYNC = {
    "soccer_epl": "football",           # Premier League
    "soccer_la_liga": "football",        # La Liga
    "soccer_serie_a": "football",        # Serie A
    "soccer_bundesliga": "football",     # Bundesliga
    "soccer_uefa_champs_league": "football",  # Champions League
    "basketball_nba": "basketball",      # NBA
    "tennis_atp": "tennis",              # ATP Tennis
    "rugby_union_super_rugby": "rugby",  # Rugby
}

def sync_upcoming_fixtures():
    """
    Fetch upcoming fixtures from The Odds API for the next 7 days.
    Creates SportsEvent + SportsMarket entries (odds) for each fixture.
    """
    API_KEY = os.environ.get("ODDS_API_KEY")
    
    if not API_KEY:
        print("❌ ODDS_API_KEY not set in environment variables")
        return False
    
    total_synced = 0
    
    for sport_code, sport_name in SPORTS_TO_SYNC.items():
        try:
            print(f"\n📡 Fetching {sport_code}...")
            
            url = "https://api.the-odds-api.com/v4/sports/{}/events".format(sport_code)
            
            response = requests.get(
                url,
                params={
                    "apiKey": API_KEY,
                    "daysFrom": 7,      # Next 7 days
                    "status": "upcoming"
                },
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"   ⚠️  API Error {response.status_code}: {response.text}")
                continue
            
            fixtures = response.json().get("events", [])
            print(f"   Found {len(fixtures)} upcoming fixtures")
            
            for fixture in fixtures:
                # Check if event already exists
                external_id = f"{sport_code}_{fixture['id']}"
                event = SportsEvent.query.filter_by(external_id=external_id).first()
                
                if event:
                    continue  # Skip if already exists
                
                # Create event
                event = SportsEvent(
                    external_id=external_id,
                    sport=sport_name,
                    league=fixture.get("league", ""),
                    home_team=fixture["home_team"],
                    away_team=fixture["away_team"],
                    event_time=datetime.fromisoformat(
                        fixture["commence_time"].replace("Z", "+00:00")
                    ),
                    status="upcoming"
                )
                db.session.add(event)
                db.session.flush()  # Get event.id
                
                # Create betting markets (Win/Draw/Loss for football, etc)
                bookmakers = fixture.get("bookmakers", [])
                
                if bookmakers:
                    # Use first bookmaker's odds
                    bookmaker = bookmakers[0]
                    markets = bookmaker.get("markets", [])
                    
                    for market in markets:
                        if market["key"] == "h2h":  # Head-to-head (win/draw/loss)
                            outcomes = market.get("outcomes", [])
                            
                            if len(outcomes) >= 2:
                                # Create market
                                sports_market = SportsMarket(
                                    event_id=event.id,
                                    market_type="h2h",
                                    status="open"
                                )
                                db.session.add(sports_market)
                                db.session.flush()
                                
                                # Create selections (home, draw, away)
                                for outcome in outcomes:
                                    selection = SportsSelection(
                                        market_id=sports_market.id,
                                        name=outcome["name"],
                                        selection_key=outcome["name"].lower().replace(" ", "_"),
                                        odds=float(outcome["price"]),
                                        status="available"
                                    )
                                    db.session.add(selection)
                
                total_synced += 1
            
            db.session.commit()
            print(f"   ✓ Synced {total_synced} fixtures so far")
        
        except Exception as e:
            print(f"   ❌ Error syncing {sport_code}: {e}")
            db.session.rollback()
            continue
    
    print(f"\n✅ Sync complete! Total fixtures: {total_synced}")
    return True


if __name__ == "__main__":
    from app import create_app
    
    app = create_app("production")
    with app.app_context():
        sync_upcoming_fixtures()
