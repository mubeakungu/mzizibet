from datetime import datetime
from flask import Blueprint, render_template, request
from flask_login import login_required

from app.models.sports import SportsEvent

sports_bp = Blueprint("sports", __name__)


@sports_bp.route("/sports")
@login_required
def lobby():
    sport = request.args.get("sport", "football")

    events = (
        SportsEvent.query.filter_by(sport=sport)
        .filter(SportsEvent.status.in_(["scheduled", "live"]))
        .order_by(SportsEvent.kickoff_at)
        .all()
    )

    return render_template("sports_lobby.html", events=events, active_sport=sport, now=datetime.utcnow())
