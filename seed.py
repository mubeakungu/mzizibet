"""
Populates game categories + catalog entries so the lobby has something to
render. This is CATALOG data only (names, categories, badges) — it does not
create any real-money-capable game, since none of these rows have a
provider_game_code set. Wire up your licensed provider's game list before
going live and update these rows with real provider_name/provider_game_code
values.

Run with: python seed.py
"""
from app.extensions import db
from app.models.casino import GameCategory, Game

CATEGORIES = [
    ("Crash Games", "crash", 1),
    ("Slots", "slots", 2),
    ("Table Games", "table", 3),
    ("Live Casino", "live", 4),
    ("Jackpots", "jackpots", 5),
]

GAMES = [
    # --- Crash Games (12) ---
    ("Aviator", "aviator", "crash", "HOT", None),
    ("Jet Crash", "jet-crash", "crash", None, None),
    ("Moon Crash", "moon-crash", "crash", "NEW", None),
    ("Mines", "mines", "crash", "POPULAR", None),
    ("Rocket X", "rocket-x", "crash", "HOT", None),
    ("Cash Blast", "cash-blast", "crash", None, None),
    ("Sky Rider", "sky-rider", "crash", "NEW", None),
    ("Meteor Rush", "meteor-rush", "crash", None, None),
    ("Multiplier Mania", "multiplier-mania", "crash", "POPULAR", None),
    ("Balloon Burst", "balloon-burst", "crash", None, None),
    ("Zeppelin", "zeppelin", "crash", "NEW", None),
    ("Comet Crash", "comet-crash", "crash", None, None),

    # --- Table Games (14) ---
    ("Plinko", "plinko", "table", "HOT", 97.0),
    ("Dice", "dice", "table", None, 98.5),
    ("Limbo", "limbo", "table", "NEW", 97.0),
    ("Wheel of Fortune", "wheel-of-fortune", "table", None, 96.5),
    ("Blackjack Classic", "blackjack-classic", "table", "POPULAR", 99.5),
    ("European Roulette", "european-roulette", "table", None, 97.3),
    ("American Roulette", "american-roulette", "table", None, 94.7),
    ("Baccarat Pro", "baccarat-pro", "table", "NEW", 98.9),
    ("Three Card Poker", "three-card-poker", "table", None, 96.6),
    ("Caribbean Stud", "caribbean-stud", "table", None, 94.8),
    ("Craps Table", "craps-table", "table", "HOT", 98.6),
    ("Hi-Lo", "hi-lo", "table", None, 97.5),
    ("Keno", "keno", "table", None, 95.0),
    ("Video Poker", "video-poker", "table", "POPULAR", 99.1),

    # --- Slots (26) ---
    ("Golden Pharaoh", "golden-pharaoh", "slots", "NEW", 97.1),
    ("Spin & Win", "spin-win", "slots", None, 95.8),
    ("Arcade Classic", "arcade-classic", "slots", "POPULAR", 96.0),
    ("Lucky Savana", "lucky-savana", "slots", "HOT", 96.5),
    ("Diamond Rush", "diamond-rush", "slots", None, 96.2),
    ("Wild Jungle", "wild-jungle", "slots", "NEW", 95.9),
    ("Fortune Tiger", "fortune-tiger", "slots", "HOT", 96.8),
    ("Sugar Rush Reels", "sugar-rush-reels", "slots", "POPULAR", 96.4),
    ("Book of Mysteries", "book-of-mysteries", "slots", None, 96.1),
    ("Fruit Frenzy", "fruit-frenzy", "slots", None, 95.5),
    ("Pirate's Treasure", "pirates-treasure", "slots", "NEW", 96.3),
    ("Viking Legends", "viking-legends", "slots", "HOT", 96.7),
    ("Mystic Forest", "mystic-forest", "slots", None, 95.7),
    ("Cleopatra's Gold", "cleopatras-gold", "slots", "POPULAR", 96.9),
    ("Samurai Storm", "samurai-storm", "slots", None, 95.6),
    ("Candy Kingdom Riches", "candy-kingdom-riches", "slots", None, 96.0),
    ("Aztec Gold", "aztec-gold", "slots", "NEW", 96.2),
    ("Starlight Spins", "starlight-spins", "slots", None, 95.9),
    ("Dragon's Fortune", "dragons-fortune", "slots", "HOT", 96.6),
    ("Safari Kingdom", "safari-kingdom", "slots", None, 96.1),
    ("Neon Nights", "neon-nights", "slots", "POPULAR", 96.4),
    ("Gold Rush Deluxe", "gold-rush-deluxe", "slots", None, 95.8),
    ("Mummy's Curse", "mummys-curse", "slots", "NEW", 96.0),
    ("Wild West Bounty", "wild-west-bounty", "slots", None, 95.7),
    ("Ocean Riches", "ocean-riches", "slots", None, 96.3),
    ("Phoenix Fire", "phoenix-fire", "slots", "HOT", 96.5),

    # --- Live Casino (10) ---
    ("Neon Roulette", "neon-roulette", "live", "NEW", 97.3),
    ("Texas Hold'em", "texas-holdem", "live", None, 98.5),
    ("Live Blackjack VIP", "live-blackjack-vip", "live", "HOT", 99.2),
    ("Live Baccarat", "live-baccarat", "live", None, 98.8),
    ("Speed Roulette", "speed-roulette", "live", "POPULAR", 97.2),
    ("Dream Wheel", "dream-wheel", "live", "NEW", 96.6),
    ("Live Sic Bo", "live-sic-bo", "live", None, 97.0),
    ("Andar Bahar Live", "andar-bahar-live", "live", None, 96.8),
    ("Live Dragon Tiger", "live-dragon-tiger", "live", "HOT", 96.9),
    ("Casino Hold'em Live", "casino-holdem-live", "live", None, 97.8),

    # --- Jackpots (8) ---
    ("Jackpot City", "jackpot-city", "jackpots", "HOT", 93.0),
    ("Mega Millions Slots", "mega-millions-slots", "jackpots", "NEW", 92.5),
    ("Progressive Fortune", "progressive-fortune", "jackpots", "POPULAR", 92.8),
    ("Diamond Jackpot", "diamond-jackpot", "jackpots", None, 93.2),
    ("Millionaire's Row", "millionaires-row", "jackpots", "HOT", 92.6),
    ("Golden Jackpot Wheel", "golden-jackpot-wheel", "jackpots", None, 93.5),
    ("Super Jackpot Slots", "super-jackpot-slots", "jackpots", "NEW", 92.9),
    ("Vault Breaker", "vault-breaker", "jackpots", None, 93.1),
]


def run(force=False):
    """Seed catalog data. Must be called inside an app context (Flask-SQLAlchemy
    needs one to talk to the DB). Idempotent — skips categories/games that
    already exist, and short-circuits entirely if the catalog is already
    populated, unless force=True. Returns True if it inserted anything."""
    if not force and Game.query.count() > 0:
        return False

    slug_to_cat = {}
    for name, slug, order in CATEGORIES:
        cat = GameCategory.query.filter_by(slug=slug).first()
        if not cat:
            cat = GameCategory(name=name, slug=slug, display_order=order)
            db.session.add(cat)
            db.session.flush()
        slug_to_cat[slug] = cat

    for i, (name, slug, cat_slug, badge, rtp) in enumerate(GAMES):
        if Game.query.filter_by(slug=slug).first():
            continue
        db.session.add(Game(
            name=name,
            slug=slug,
            category_id=slug_to_cat[cat_slug].id,
            badge=badge,
            rtp_percent=rtp,
            display_order=i,
            is_active=True,
        ))

    db.session.commit()
    return True


if __name__ == "__main__":
    # Only build an app (and thus a DB connection) when run directly, e.g.
    # `python seed.py` for a manual/local seed against DATABASE_URL.
    from app import create_app

    app = create_app("development")
    with app.app_context():
        db.create_all()
        if run(force=True):
            print(f"Seeded {len(CATEGORIES)} categories and {len(GAMES)} games.")
        else:
            print("Catalog already populated — nothing to do.")
