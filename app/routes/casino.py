from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.models.casino import Game, GameCategory

casino_bp = Blueprint("casino", __name__)


@casino_bp.route("/casino")
@login_required
def lobby():
    category_slug = request.args.get("category", "all")
    search = request.args.get("q", "").strip()

    categories = GameCategory.query.order_by(GameCategory.display_order).all()

    query = Game.query.filter_by(is_active=True)
    if category_slug != "all":
        query = query.join(GameCategory).filter(GameCategory.slug == category_slug)
    if search:
        query = query.filter(Game.name.ilike(f"%{search}%"))

    games = query.order_by(Game.display_order).all()

    return render_template(
        "casino_lobby.html",
        categories=categories,
        games=games,
        active_category=category_slug,
        search=search,
    )


@casino_bp.route("/casino/play/<slug>")
@login_required
def play(slug):
    game = Game.query.filter_by(slug=slug, is_active=True).first_or_404()

    can_play, reason = current_user.can_play()
    if not can_play:
        return render_template("casino_blocked.html", reason=reason)

    # Real launch: hand off to the licensed provider's game-launch URL,
    # built from game.provider_name / game.provider_game_code + a signed
    # session token. Intentionally not stubbed here — see README.
    return render_template("casino_play.html", game=game)
