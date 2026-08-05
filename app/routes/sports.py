# Add/update your app/routes/sports.py with this code

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models.sports import SportsEvent, SportsMarket, SportsSelection, Bet, BetSlip, BetSlipLeg
from datetime import datetime, timedelta

sports_bp = Blueprint("sports", __name__, url_prefix="/sports")


@sports_bp.route("/")
@sports_bp.route("/lobby")
def lobby():
    """Display upcoming sports fixtures for betting."""
    
    # Get filter parameters
    active_sport = request.args.get("sport", "all")
    search = request.args.get("q", "").strip()
    
    # Query upcoming events (next 7 days)
    query = SportsEvent.query.filter(
        SportsEvent.event_time >= datetime.utcnow(),
        SportsEvent.event_time <= datetime.utcnow() + timedelta(days=7),
        SportsEvent.status == "upcoming"
    )
    
    # Filter by sport
    if active_sport != "all":
        query = query.filter_by(sport=active_sport)
    
    # Search by team name
    if search:
        query = query.filter(
            db.or_(
                SportsEvent.home_team.ilike(f"%{search}%"),
                SportsEvent.away_team.ilike(f"%{search}%")
            )
        )
    
    # Order by event time
    upcoming_events = query.order_by(SportsEvent.event_time.asc()).all()
    
    # Get unique sports for filter tabs
    all_sports = db.session.query(SportsEvent.sport).filter(
        SportsEvent.event_time >= datetime.utcnow()
    ).distinct().all()
    sports = [s[0] for s in all_sports]
    
    return render_template(
        "sports_lobby.html",
        upcoming_events=upcoming_events,
        active_sport=active_sport,
        sports=sports,
        search=search
    )


@sports_bp.route("/event/<int:event_id>")
def event_detail(event_id):
    """Show detailed view of an event with all available markets."""
    event = SportsEvent.query.get_or_404(event_id)
    
    return render_template(
        "sports_event_detail.html",
        event=event
    )


@sports_bp.route("/place-bet/<int:event_id>", methods=["GET", "POST"])
@login_required
def place_bet(event_id):
    """Handle bet placement."""
    event = SportsEvent.query.get_or_404(event_id)
    selection_id = request.args.get("selection_id", type=int)
    
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount", 0))
            selection_id = int(request.form.get("selection_id", 0))
            
            if amount <= 0 or amount > current_user.wallet.balance:
                return jsonify({"error": "Invalid amount"}), 400
            
            selection = SportsSelection.query.get_or_404(selection_id)
            market = SportsMarket.query.get(selection.market_id)
            
            # Create bet slip
            bet_slip = BetSlip(
                user_id=current_user.id,
                status="open",
                potential_return=amount * selection.odds
            )
            db.session.add(bet_slip)
            db.session.flush()
            
            # Add leg to bet slip
            leg = BetSlipLeg(
                bet_slip_id=bet_slip.id,
                event_id=event_id,
                market_id=market.id,
                selection_id=selection_id,
                odds=selection.odds,
                status="pending"
            )
            db.session.add(leg)
            
            # Create actual bet (place immediately or hold in slip)
            bet = Bet(
                user_id=current_user.id,
                bet_slip_id=bet_slip.id,
                amount=amount,
                potential_return=amount * selection.odds,
                status="pending"
            )
            db.session.add(bet)
            
            # Deduct from wallet
            current_user.wallet.balance -= amount
            
            db.session.commit()
            
            return redirect(url_for("sports.bet_confirmation", bet_id=bet.id))
        
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    
    # GET: Show bet placement form
    return render_template(
        "sports_place_bet.html",
        event=event,
        selection_id=selection_id
    )


@sports_bp.route("/bet-confirmation/<int:bet_id>")
@login_required
def bet_confirmation(bet_id):
    """Show bet confirmation page."""
    bet = Bet.query.get_or_404(bet_id)
    
    # Only show own bets
    if bet.user_id != current_user.id:
        return redirect(url_for("sports.lobby"))
    
    return render_template(
        "sports_bet_confirmation.html",
        bet=bet
    )


@sports_bp.route("/my-bets")
@login_required
def my_bets():
    """Show user's active and settled bets."""
    page = request.args.get("page", 1, type=int)
    
    bets = Bet.query.filter_by(user_id=current_user.id).order_by(
        Bet.created_at.desc()
    ).paginate(page=page, per_page=20)
    
    return render_template(
        "sports_my_bets.html",
        bets=bets
    )


@sports_bp.route("/api/odds/<int:selection_id>")
def get_odds(selection_id):
    """API endpoint to get real-time odds (for dynamic updates)."""
    selection = SportsSelection.query.get_or_404(selection_id)
    
    return jsonify({
        "name": selection.name,
        "odds": float(selection.odds),
        "status": selection.status
    })
