from flask import Flask, redirect, url_for
from flask_login import current_user
from config import config
from app.extensions import db, login_manager, migrate, bcrypt


def _seed_catalog_if_empty():
    """Populate game categories + catalog entries the first time the app
    boots against an empty database. Catalog data only (names, categories,
    badges) — no real-money-capable rows, since none have a
    provider_game_code set. Delegates to seed.py's run(), which is a no-op
    if the catalog already has games."""
    import seed
    seed.run()


def _update_game_thumbnails():
    """Update existing games with thumbnail URLs on startup."""
    from app.models.casino import Game

    GAME_IMAGES = {
        # Crash Games
        "aviator": "https://placehold.co/400x500?text=Aviator&font=raleway&bg=1a1a2e&textbg=0f3460",
        "jet-crash": "https://placehold.co/400x500?text=Jet+Crash&font=raleway&bg=16213e&textbg=0f3460",
        "moon-crash": "https://placehold.co/400x500?text=Moon+Crash&font=raleway&bg=0f3460&textbg=16213e",
        "mines": "https://placehold.co/400x500?text=Mines&font=raleway&bg=1a1a2e&textbg=e94560",
        "rocket-x": "https://placehold.co/400x500?text=Rocket+X&font=raleway&bg=16213e&textbg=0f3460",
        "cash-blast": "https://placehold.co/400x500?text=Cash+Blast&font=raleway&bg=0f3460&textbg=16213e",
        "sky-rider": "https://placehold.co/400x500?text=Sky+Rider&font=raleway&bg=1a1a2e&textbg=e94560",
        "meteor-rush": "https://placehold.co/400x500?text=Meteor+Rush&font=raleway&bg=16213e&textbg=0f3460",
        "multiplier-mania": "https://placehold.co/400x500?text=Multiplier+Mania&font=raleway&bg=0f3460&textbg=16213e",
        "balloon-burst": "https://placehold.co/400x500?text=Balloon+Burst&font=raleway&bg=1a1a2e&textbg=e94560",
        "zeppelin": "https://placehold.co/400x500?text=Zeppelin&font=raleway&bg=16213e&textbg=0f3460",
        "comet-crash": "https://placehold.co/400x500?text=Comet+Crash&font=raleway&bg=0f3460&textbg=16213e",

        # Table Games
        "plinko": "https://placehold.co/400x500?text=Plinko&font=raleway&bg=1a472a&textbg=2d5a3d",
        "dice": "https://placehold.co/400x500?text=Dice&font=raleway&bg=2d5a3d&textbg=1a472a",
        "limbo": "https://placehold.co/400x500?text=Limbo&font=raleway&bg=1a472a&textbg=2d5a3d",
        "wheel-of-fortune": "https://placehold.co/400x500?text=Wheel+of+Fortune&font=raleway&bg=2d5a3d&textbg=1a472a",
        "blackjack-classic": "https://placehold.co/400x500?text=Blackjack&font=raleway&bg=1a472a&textbg=2d5a3d",
        "european-roulette": "https://placehold.co/400x500?text=EU+Roulette&font=raleway&bg=2d5a3d&textbg=1a472a",
        "american-roulette": "https://placehold.co/400x500?text=US+Roulette&font=raleway&bg=1a472a&textbg=2d5a3d",
        "baccarat-pro": "https://placehold.co/400x500?text=Baccarat+Pro&font=raleway&bg=2d5a3d&textbg=1a472a",
        "three-card-poker": "https://placehold.co/400x500?text=3+Card+Poker&font=raleway&bg=1a472a&textbg=2d5a3d",
        "caribbean-stud": "https://placehold.co/400x500?text=Caribbean+Stud&font=raleway&bg=2d5a3d&textbg=1a472a",
        "craps-table": "https://placehold.co/400x500?text=Craps&font=raleway&bg=1a472a&textbg=2d5a3d",
        "hi-lo": "https://placehold.co/400x500?text=Hi-Lo&font=raleway&bg=2d5a3d&textbg=1a472a",
        "keno": "https://placehold.co/400x500?text=Keno&font=raleway&bg=1a472a&textbg=2d5a3d",
        "video-poker": "https://placehold.co/400x500?text=Video+Poker&font=raleway&bg=2d5a3d&textbg=1a472a",

        # Slots
        "golden-pharaoh": "https://placehold.co/400x500?text=Golden+Pharaoh&font=raleway&bg=4a3728&textbg=7a5c42",
        "spin-win": "https://placehold.co/400x500?text=Spin+%26+Win&font=raleway&bg=7a5c42&textbg=4a3728",
        "arcade-classic": "https://placehold.co/400x500?text=Arcade+Classic&font=raleway&bg=4a3728&textbg=7a5c42",
        "lucky-savana": "https://placehold.co/400x500?text=Lucky+Savana&font=raleway&bg=7a5c42&textbg=4a3728",
        "diamond-rush": "https://placehold.co/400x500?text=Diamond+Rush&font=raleway&bg=4a3728&textbg=7a5c42",
        "wild-jungle": "https://placehold.co/400x500?text=Wild+Jungle&font=raleway&bg=7a5c42&textbg=4a3728",
        "fortune-tiger": "https://placehold.co/400x500?text=Fortune+Tiger&font=raleway&bg=4a3728&textbg=7a5c42",
        "sugar-rush-reels": "https://placehold.co/400x500?text=Sugar+Rush&font=raleway&bg=7a5c42&textbg=4a3728",
        "book-of-mysteries": "https://placehold.co/400x500?text=Book+of+Mysteries&font=raleway&bg=4a3728&textbg=7a5c42",
        "fruit-frenzy": "https://placehold.co/400x500?text=Fruit+Frenzy&font=raleway&bg=7a5c42&textbg=4a3728",
        "pirates-treasure": "https://placehold.co/400x500?text=Pirates+Treasure&font=raleway&bg=4a3728&textbg=7a5c42",
        "viking-legends": "https://placehold.co/400x500?text=Viking+Legends&font=raleway&bg=7a5c42&textbg=4a3728",
        "mystic-forest": "https://placehold.co/400x500?text=Mystic+Forest&font=raleway&bg=4a3728&textbg=7a5c42",
        "cleopatras-gold": "https://placehold.co/400x500?text=Cleopatras+Gold&font=raleway&bg=7a5c42&textbg=4a3728",
        "samurai-storm": "https://placehold.co/400x500?text=Samurai+Storm&font=raleway&bg=4a3728&textbg=7a5c42",
        "candy-kingdom-riches": "https://placehold.co/400x500?text=Candy+Kingdom&font=raleway&bg=7a5c42&textbg=4a3728",
        "aztec-gold": "https://placehold.co/400x500?text=Aztec+Gold&font=raleway&bg=4a3728&textbg=7a5c42",
        "starlight-spins": "https://placehold.co/400x500?text=Starlight+Spins&font=raleway&bg=7a5c42&textbg=4a3728",
        "dragons-fortune": "https://placehold.co/400x500?text=Dragons+Fortune&font=raleway&bg=4a3728&textbg=7a5c42",
        "safari-kingdom": "https://placehold.co/400x500?text=Safari+Kingdom&font=raleway&bg=7a5c42&textbg=4a3728",
        "neon-nights": "https://placehold.co/400x500?text=Neon+Nights&font=raleway&bg=4a3728&textbg=7a5c42",
        "gold-rush-deluxe": "https://placehold.co/400x500?text=Gold+Rush&font=raleway&bg=7a5c42&textbg=4a3728",
        "mummys-curse": "https://placehold.co/400x500?text=Mummys+Curse&font=raleway&bg=4a3728&textbg=7a5c42",
        "wild-west-bounty": "https://placehold.co/400x500?text=Wild+West&font=raleway&bg=7a5c42&textbg=4a3728",
        "ocean-riches": "https://placehold.co/400x500?text=Ocean+Riches&font=raleway&bg=4a3728&textbg=7a5c42",
        "phoenix-fire": "https://placehold.co/400x500?text=Phoenix+Fire&font=raleway&bg=7a5c42&textbg=4a3728",

        # Live Casino
        "neon-roulette": "https://placehold.co/400x500?text=Neon+Roulette&font=raleway&bg=2d1b4e&textbg=5a3a8a",
        "texas-holdem": "https://placehold.co/400x500?text=Texas+Holdem&font=raleway&bg=5a3a8a&textbg=2d1b4e",
        "live-blackjack-vip": "https://placehold.co/400x500?text=Live+Blackjack&font=raleway&bg=2d1b4e&textbg=5a3a8a",
        "live-baccarat": "https://placehold.co/400x500?text=Live+Baccarat&font=raleway&bg=5a3a8a&textbg=2d1b4e",
        "speed-roulette": "https://placehold.co/400x500?text=Speed+Roulette&font=raleway&bg=2d1b4e&textbg=5a3a8a",
        "dream-wheel": "https://placehold.co/400x500?text=Dream+Wheel&font=raleway&bg=5a3a8a&textbg=2d1b4e",
        "live-sic-bo": "https://placehold.co/400x500?text=Live+Sic+Bo&font=raleway&bg=2d1b4e&textbg=5a3a8a",
        "andar-bahar-live": "https://placehold.co/400x500?text=Andar+Bahar&font=raleway&bg=5a3a8a&textbg=2d1b4e",
        "live-dragon-tiger": "https://placehold.co/400x500?text=Dragon+Tiger&font=raleway&bg=2d1b4e&textbg=5a3a8a",
        "casino-holdem-live": "https://placehold.co/400x500?text=Casino+Holdem&font=raleway&bg=5a3a8a&textbg=2d1b4e",

        # Jackpots
        "jackpot-city": "https://placehold.co/400x500?text=Jackpot+City&font=raleway&bg=4a2c1a&textbg=8b5a2b",
        "mega-millions-slots": "https://placehold.co/400x500?text=Mega+Millions&font=raleway&bg=8b5a2b&textbg=4a2c1a",
        "progressive-fortune": "https://placehold.co/400x500?text=Progressive&font=raleway&bg=4a2c1a&textbg=8b5a2b",
        "diamond-jackpot": "https://placehold.co/400x500?text=Diamond+Jackpot&font=raleway&bg=8b5a2b&textbg=4a2c1a",
        "millionaires-row": "https://placehold.co/400x500?text=Millionaires+Row&font=raleway&bg=4a2c1a&textbg=8b5a2b",
        "golden-jackpot-wheel": "https://placehold.co/400x500?text=Golden+Jackpot&font=raleway&bg=8b5a2b&textbg=4a2c1a",
        "super-jackpot-slots": "https://placehold.co/400x500?text=Super+Jackpot&font=raleway&bg=4a2c1a&textbg=8b5a2b",
        "vault-breaker": "https://placehold.co/400x500?text=Vault+Breaker&font=raleway&bg=8b5a2b&textbg=4a2c1a",
    }

    updated = 0
    for slug, url in GAME_IMAGES.items():
        game = Game.query.filter_by(slug=slug).first()
        if game and not game.thumbnail_url:
            game.thumbnail_url = url
            updated += 1

    if updated > 0:
        db.session.commit()


def _sync_sports_if_needed():
    """Sync sports fixtures on app startup if database is empty or stale."""
    import requests
    import os
    from datetime import datetime, timedelta
    from app.models.sports import SportsEvent, SportsMarket, SportsSelection

    # Only sync if older than 1 hour
    last_event = SportsEvent.query.order_by(SportsEvent.created_at.desc()).first()
    if last_event and (datetime.utcnow() - last_event.created_at) < timedelta(hours=1):
        return

    API_KEY = os.environ.get("ODDS_API_KEY")
    if not API_KEY:
        return

    SPORTS = ["soccer_epl", "basketball_nba", "tennis_atp"]
    total = 0

    for sport_code in SPORTS:
        try:
            response = requests.get(
                f"https://api.the-odds-api.com/v4/sports/{sport_code}/events",
                params={"apiKey": API_KEY, "daysFrom": 7},
                timeout=10
            )
            if response.status_code != 200:
                continue

            for fixture in response.json().get("events", []):
                external_id = f"{sport_code}_{fixture['id']}"
                if SportsEvent.query.filter_by(external_id=external_id).first():
                    continue

                event = SportsEvent(
                    external_id=external_id,
                    sport=sport_code.split("_")[0],
                    home_team=fixture["home_team"],
                    away_team=fixture["away_team"],
                    event_time=datetime.fromisoformat(fixture["commence_time"].replace("Z", "+00:00")),
                    status="upcoming"
                )
                db.session.add(event)
                db.session.flush()

                # Add odds from bookmakers
                for bookie in fixture.get("bookmakers", [])[:1]:
                    for market in bookie.get("markets", []):
                        if market["key"] == "h2h":
                            market_obj = SportsMarket(event_id=event.id, market_type="h2h")
                            db.session.add(market_obj)
                            db.session.flush()

                            for outcome in market.get("outcomes", []):
                                sel = SportsSelection(
                                    market_id=market_obj.id,
                                    name=outcome["name"],
                                    selection_key=outcome["name"].lower().replace(" ", "_"),
                                    odds=float(outcome["price"]),
                                    status="available"
                                )
                                db.session.add(sel)

                total += 1

            db.session.commit()
        except Exception:
            db.session.rollback()

    if total > 0:
        print(f"✓ Synced {total} sports fixtures")


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Import every model module so SQLAlchemy knows about all tables before
    # create_all() runs below.
    from app.models.user import User
    from app.models.wallet import Wallet, Transaction  # noqa: F401
    from app.models.casino import GameCategory, Game, CasinoRound  # noqa: F401
    from app.models.sports import (  # noqa: F401
        SportsEvent, SportsMarket, SportsSelection, BetSlip, BetSlipLeg, Bet,
    )

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    from app.routes.auth import auth_bp
    from app.routes.casino import casino_bp
    from app.routes.sports import sports_bp
    from app.routes.wallet import wallet_bp
    from app.routes.admin import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(casino_bp)
    app.register_blueprint(sports_bp)
    app.register_blueprint(wallet_bp, url_prefix="/wallet")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # --- Auto-create tables + seed catalog data + sync live sports --------
    # No Flask-Migrate migrations exist yet, and Render's free tier gives no
    # shell access to run `flask db upgrade` / `python seed.py` by hand. So
    # do it here, once, at startup. create_all() is a no-op for tables that
    # already exist, the seed check only inserts rows if the catalog is
    # empty, and the sports sync only hits the API if data is missing or
    # more than an hour old — so this is safe to run on every restart/deploy.
    with app.app_context():
        db.create_all()
        _seed_catalog_if_empty()
        _update_game_thumbnails()
        _sync_sports_if_needed()

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("casino.lobby"))
        return redirect(url_for("auth.login"))

    @app.context_processor
    def inject_globals():
        return {
            "site_name": "Mzizibet",
            "default_showcase_games": [
                {"name": "Aviator", "badge": "HOT", "thumbnail_url": None},
                {"name": "Fortune Tiger", "badge": "HOT", "thumbnail_url": None},
                {"name": "Mines", "badge": "POPULAR", "thumbnail_url": None},
                {"name": "Plinko", "badge": "HOT", "thumbnail_url": None},
                {"name": "European Roulette", "badge": None, "thumbnail_url": None},
                {"name": "Live Blackjack VIP", "badge": "HOT", "thumbnail_url": None},
            ],
        }

    return app
