from datetime import datetime
from app.extensions import db


class SportsEvent(db.Model):
    """
    Fixture list. Populated from a licensed odds/data feed — do not
    hand-enter odds for real-money markets outside that feed.
    """

    __tablename__ = "sports_events"

    id = db.Column(db.Integer, primary_key=True)
    sport = db.Column(db.String(40), nullable=False)  # football, basketball, tennis, rugby...
    league = db.Column(db.String(120), nullable=False)
    home_team = db.Column(db.String(120), nullable=False)
    away_team = db.Column(db.String(120), nullable=False)
    kickoff_at = db.Column(db.DateTime, nullable=False)

    provider_event_id = db.Column(db.String(120), nullable=True)  # feed's own ID
    status = db.Column(db.String(20), default="scheduled")  # scheduled, live, finished, postponed

    markets = db.relationship("SportsMarket", backref="event", lazy="dynamic")


class SportsMarket(db.Model):
    """A bettable market on an event, e.g. '1X2', 'Over/Under 2.5'."""

    __tablename__ = "sports_markets"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("sports_events.id"), nullable=False)
    market_type = db.Column(db.String(60), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    selections = db.relationship("SportsSelection", backref="market", lazy="dynamic")


class SportsSelection(db.Model):
    """One outcome within a market, with the current odds from the feed."""

    __tablename__ = "sports_selections"

    id = db.Column(db.Integer, primary_key=True)
    market_id = db.Column(db.Integer, db.ForeignKey("sports_markets.id"), nullable=False)
    label = db.Column(db.String(80), nullable=False)  # "Home", "Draw", "Over 2.5"
    odds = db.Column(db.Numeric(6, 2), nullable=False)
    result = db.Column(db.String(10), nullable=True)  # won, lost, void — set on settlement


class BetSlip(db.Model):
    """A single bet slip — one or more selections (single or multibet)."""

    __tablename__ = "bet_slips"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    stake = db.Column(db.Numeric(12, 2), nullable=False)
    total_odds = db.Column(db.Numeric(8, 2), nullable=False)
    potential_payout = db.Column(db.Numeric(12, 2), nullable=False)

    status = db.Column(db.String(20), default="pending")  # pending, won, lost, void, cashed_out
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    settled_at = db.Column(db.DateTime, nullable=True)

    legs = db.relationship("BetSlipLeg", backref="slip", cascade="all, delete-orphan")


class BetSlipLeg(db.Model):
    __tablename__ = "bet_slip_legs"

    id = db.Column(db.Integer, primary_key=True)
    slip_id = db.Column(db.Integer, db.ForeignKey("bet_slips.id"), nullable=False)
    selection_id = db.Column(db.Integer, db.ForeignKey("sports_selections.id"), nullable=False)
    odds_at_placement = db.Column(db.Numeric(6, 2), nullable=False)
    result = db.Column(db.String(10), nullable=True)


# Kept separate from casino/sports for a simple unified "my bets" query
class Bet(db.Model):
    __tablename__ = "bets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bet_type = db.Column(db.String(10), nullable=False)  # 'casino' or 'sports'
    reference_id = db.Column(db.Integer, nullable=False)  # CasinoRound.id or BetSlip.id
    stake = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
