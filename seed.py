"""
Populates game categories + catalog entries so the lobby has something to
render. This is CATALOG data only (names, categories, badges) — it does not
create any real-money-capable game, since none of these rows have a
provider_game_code set. Wire up your licensed provider's game list before
going live and update these rows with real provider_name/provider_game_code
values.

Run with: python seed.py

NOTE: Make sure your Game model has an `image_url` field. If not, add:
    image_url = db.Column(db.String(500), nullable=True)
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
    # Format: (name, slug, category, badge, rtp, image_url)
    
    # --- Crash Games (12) ---
    ("Aviator", "aviator", "crash", "HOT", None, "https://placehold.co/400x500?text=Aviator&font=raleway&bg=1a1a2e&textbg=0f3460"),
    ("Jet Crash", "jet-crash", "crash", None, None, "https://placehold.co/400x500?text=Jet+Crash&font=raleway&bg=16213e&textbg=0f3460"),
    ("Moon Crash", "moon-crash", "crash", "NEW", None, "https://placehold.co/400x500?text=Moon+Crash&font=raleway&bg=0f3460&textbg=16213e"),
    ("Mines", "mines", "crash", "POPULAR", None, "https://placehold.co/400x500?text=Mines&font=raleway&bg=1a1a2e&textbg=e94560"),
    ("Rocket X", "rocket-x", "crash", "HOT", None, "https://placehold.co/400x500?text=Rocket+X&font=raleway&bg=16213e&textbg=0f3460"),
    ("Cash Blast", "cash-blast", "crash", None, None, "https://placehold.co/400x500?text=Cash+Blast&font=raleway&bg=0f3460&textbg=16213e"),
    ("Sky Rider", "sky-rider", "crash", "NEW", None, "https://placehold.co/400x500?text=Sky+Rider&font=raleway&bg=1a1a2e&textbg=e94560"),
    ("Meteor Rush", "meteor-rush", "crash", None, None, "https://placehold.co/400x500?text=Meteor+Rush&font=raleway&bg=16213e&textbg=0f3460"),
    ("Multiplier Mania", "multiplier-mania", "crash", "POPULAR", None, "https://placehold.co/400x500?text=Multiplier+Mania&font=raleway&bg=0f3460&textbg=16213e"),
    ("Balloon Burst", "balloon-burst", "crash", None, None, "https://placehold.co/400x500?text=Balloon+Burst&font=raleway&bg=1a1a2e&textbg=e94560"),
    ("Zeppelin", "zeppelin", "crash", "NEW", None, "https://placehold.co/400x500?text=Zeppelin&font=raleway&bg=16213e&textbg=0f3460"),
    ("Comet Crash", "comet-crash", "crash", None, None, "https://placehold.co/400x500?text=Comet+Crash&font=raleway&bg=0f3460&textbg=16213e"),

    # --- Table Games (14) ---
    ("Plinko", "plinko", "table", "HOT", 97.0, "https://placehold.co/400x500?text=Plinko&font=raleway&bg=1a472a&textbg=2d5a3d"),
    ("Dice", "dice", "table", None, 98.5, "https://placehold.co/400x500?text=Dice&font=raleway&bg=2d5a3d&textbg=1a472a"),
    ("Limbo", "limbo", "table", "NEW", 97.0, "https://placehold.co/400x500?text=Limbo&font=raleway&bg=1a472a&textbg=2d5a3d"),
    ("Wheel of Fortune", "wheel-of-fortune", "table", None, 96.5, "https://placehold.co/400x500?text=Wheel+of+Fortune&font=raleway&bg=2d5a3d&textbg=1a472a"),
    ("Blackjack Classic", "blackjack-classic", "table", "POPULAR", 99.5, "https://placehold.co/400x500?text=Blackjack&font=raleway&bg=1a472a&textbg=2d5a3d"),
    ("European Roulette", "european-roulette", "table", None, 97.3, "https://placehold.co/400x500?text=EU+Roulette&font=raleway&bg=2d5a3d&textbg=1a472a"),
    ("American Roulette", "american-roulette", "table", None, 94.7, "https://placehold.co/400x500?text=US+Roulette&font=raleway&bg=1a472a&textbg=2d5a3d"),
    ("Baccarat Pro", "baccarat-pro", "table", "NEW", 98.9, "https://placehold.co/400x500?text=Baccarat+Pro&font=raleway&bg=2d5a3d&textbg=1a472a"),
    ("Three Card Poker", "three-card-poker", "table", None, 96.6, "https://placehold.co/400x500?text=3+Card+Poker&font=raleway&bg=1a472a&textbg=2d5a3d"),
    ("Caribbean Stud", "caribbean-stud", "table", None, 94.8, "https://placehold.co/400x500?text=Caribbean+Stud&font=raleway&bg=2d5a3d&textbg=1a472a"),
    ("Craps Table", "craps-table", "table", "HOT", 98.6, "https://placehold.co/400x500?text=Craps&font=raleway&bg=1a472a&textbg=2d5a3d"),
    ("Hi-Lo", "hi-lo", "table", None, 97.5, "https://placehold.co/400x500?text=Hi-Lo&font=raleway&bg=2d5a3d&textbg=1a472a"),
    ("Keno", "keno", "table", None, 95.0, "https://placehold.co/400x500?text=Keno&font=raleway&bg=1a472a&textbg=2d5a3d"),
    ("Video Poker", "video-poker", "table", "POPULAR", 99.1, "https://placehold.co/400x500?text=Video+Poker&font=raleway&bg=2d5a3d&textbg=1a472a"),

    # --- Slots (26) ---
    ("Golden Pharaoh", "golden-pharaoh", "slots", "NEW", 97.1, "https://placehold.co/400x500?text=Golden+Pharaoh&font=raleway&bg=4a3728&textbg=7a5c42"),
    ("Spin & Win", "spin-win", "slots", None, 95.8, "https://placehold.co/400x500?text=Spin+%26+Win&font=raleway&bg=7a5c42&textbg=4a3728"),
    ("Arcade Classic", "arcade-classic", "slots", "POPULAR", 96.0, "https://placehold.co/400x500?text=Arcade+Classic&font=raleway&bg=4a3728&textbg=7a5c42"),
    ("Lucky Savana", "lucky-savana", "slots", "HOT", 96.5, "https://placehold.co/400x500?text=Lucky+Savana&font=raleway&bg=7a5c42&textbg=4a3728"),
    ("Diamond Rush", "diamond-rush", "slots", None, 96.2, "https://placehold.co/400x500?text=Diamond+Rush&font=raleway&bg=4a3728&textbg=7a5c42"),
    ("Wild Jungle", "wild-jungle", "slots", "NEW", 95.9, "https://placehold.co/400x500?text=Wild+Jungle&font=raleway&bg=7a5c42&textbg=4a3728"),
    ("Fortune Tiger", "fortune-tiger", "slots", "HOT", 96.8, "https://placehold.co/400x500?text=Fortune+Tiger&font=raleway&bg=4a3728&textbg=7a5c42"),
    ("Sugar Rush Reels", "sugar-rush-reels", "slots", "POPULAR", 96.4, "https://placehold.co/400x500?text=Sugar+Rush&font=raleway&bg=7a5c42&textbg=4a3728"),
    ("Book of Mysteries", "book-of-mysteries", "slots", None, 96.1, "https://placehold.co/400x500?text=Book+of+Mysteries&font=raleway&bg=4a3728&textbg=7a5c42"),
    ("Fruit Frenzy", "fruit-frenzy", "slots", None, 95.5, "https://placehold.co/400x500?text=Fruit+Frenzy&font=raleway&bg=7a5c42&textbg=4a3728"),
    ("Pirate's Treasure", "pirates-treasure", "slots", "NEW", 96.3, "https://placehold.co/400x500?text=Pirates+Treasure&font=raleway&bg=4a3728&textbg=7a5c42"),
    ("Viking Legends", "viking-legends", "slots", "HOT", 96.7, "https://placehold.co/400x500?text=Viking+Legends&font=raleway&bg=7a5c42&textbg=4a3728"),
    ("Mystic Forest", "mystic-forest", "slots", None, 95.7, "https://placehold.co/400x500?text=Mystic+Forest&font=raleway&bg=4a3728&textbg=7a5c42"),
    ("Cleopatra's Gold", "cleopatras-gold", "slots", "POPULAR", 96.9, "https://placehold.co/400x500?text=Cleopatras+Gold&font=raleway&bg=7a5c42&textbg=4a3728"),
    ("Samurai Storm", "samurai-storm", "slots", None, 95.6, "https://placehold.co/400x500?text=Samurai+Storm&font=raleway&bg=4a3728&textbg=7a5c42"),
    ("Candy Kingdom Riches", "candy-kingdom-riches", "slots", None, 96.0, "https://placehold.co/400x500?text=Candy+Kingdom&font=raleway&bg=7a5c42&textbg=4a3728"),
    ("Aztec Gold", "aztec-gold", "slots", "NEW", 96.2, "https://placehold.co/400x500?text=Aztec+Gold&font=raleway&bg=4a3728&textbg=7a5c42"),
    ("Starlight Spins", "starlight-spins", "slots", None, 95.9, "https://placehold.co/400x500?text=Starlight+Spins&font=raleway&bg=7a5c42&textbg=4a3728"),
    ("Dragon's Fortune", "dragons-fortune", "slots", "HOT", 96.6, "https://placehold.co/400x500?text=Dragons+Fortune&font=raleway&bg=4a3728&textbg=7a5c42"),
    ("Safari Kingdom", "safari-kingdom", "slots", None, 96.1, "https://placehold.co/400x500?text=Safari+Kingdom&font=raleway&bg=7a5c42&textbg=4a3728"),
    ("Neon Nights", "neon-nights", "slots", "POPULAR", 96.4, "https://placehold.co/400x500?text=Neon+Nights&font=raleway&bg=4a3728&textbg=7a5c42"),
    ("Gold Rush Deluxe", "gold-rush-deluxe", "slots", None, 95.8, "https://placehold.co/400x500?text=Gold+Rush&font=raleway&bg=7a5c42&textbg=4a3728"),
    ("Mummy's Curse", "mummys-curse", "slots", "NEW", 96.0, "https://placehold.co/400x500?text=Mummys+Curse&font=raleway&bg=4a3728&textbg=7a5c42"),
    ("Wild West Bounty", "wild-west-bounty", "slots", None, 95.7, "https://placehold.co/400x500?text=Wild+West&font=raleway&bg=7a5c42&textbg=4a3728"),
    ("Ocean Riches", "ocean-riches", "slots", None, 96.3, "https://placehold.co/400x500?text=Ocean+Riches&font=raleway&bg=4a3728&textbg=7a5c42"),
    ("Phoenix Fire", "phoenix-fire", "slots", "HOT", 96.5, "https://placehold.co/400x500?text=Phoenix+Fire&font=raleway&bg=7a5c42&textbg=4a3728"),

    # --- Live Casino (10) ---
    ("Neon Roulette", "neon-roulette", "live", "NEW", 97.3, "https://placehold.co/400x500?text=Neon+Roulette&font=raleway&bg=2d1b4e&textbg=5a3a8a"),
    ("Texas Hold'em", "texas-holdem", "live", None, 98.5, "https://placehold.co/400x500?text=Texas+Holdem&font=raleway&bg=5a3a8a&textbg=2d1b4e"),
    ("Live Blackjack VIP", "live-blackjack-vip", "live", "HOT", 99.2, "https://placehold.co/400x500?text=Live+Blackjack&font=raleway&bg=2d1b4e&textbg=5a3a8a"),
    ("Live Baccarat", "live-baccarat", "live", None, 98.8, "https://placehold.co/400x500?text=Live+Baccarat&font=raleway&bg=5a3a8a&textbg=2d1b4e"),
    ("Speed Roulette", "speed-roulette", "live", "POPULAR", 97.2, "https://placehold.co/400x500?text=Speed+Roulette&font=raleway&bg=2d1b4e&textbg=5a3a8a"),
    ("Dream Wheel", "dream-wheel", "live", "NEW", 96.6, "https://placehold.co/400x500?text=Dream+Wheel&font=raleway&bg=5a3a8a&textbg=2d1b4e"),
    ("Live Sic Bo", "live-sic-bo", "live", None, 97.0, "https://placehold.co/400x500?text=Live+Sic+Bo&font=raleway&bg=2d1b4e&textbg=5a3a8a"),
    ("Andar Bahar Live", "andar-bahar-live", "live", None, 96.8, "https://placehold.co/400x500?text=Andar+Bahar&font=raleway&bg=5a3a8a&textbg=2d1b4e"),
    ("Live Dragon Tiger", "live-dragon-tiger", "live", "HOT", 96.9, "https://placehold.co/400x500?text=Dragon+Tiger&font=raleway&bg=2d1b4e&textbg=5a3a8a"),
    ("Casino Hold'em Live", "casino-holdem-live", "live", None, 97.8, "https://placehold.co/400x500?text=Casino+Holdem&font=raleway&bg=5a3a8a&textbg=2d1b4e"),

    # --- Jackpots (8) ---
    ("Jackpot City", "jackpot-city", "jackpots", "HOT", 93.0, "https://placehold.co/400x500?text=Jackpot+City&font=raleway&bg=4a2c1a&textbg=8b5a2b"),
    ("Mega Millions Slots", "mega-millions-slots", "jackpots", "NEW", 92.5, "https://placehold.co/400x500?text=Mega+Millions&font=raleway&bg=8b5a2b&textbg=4a2c1a"),
    ("Progressive Fortune", "progressive-fortune", "jackpots", "POPULAR", 92.8, "https://placehold.co/400x500?text=Progressive&font=raleway&bg=4a2c1a&textbg=8b5a2b"),
    ("Diamond Jackpot", "diamond-jackpot", "jackpots", None, 93.2, "https://placehold.co/400x500?text=Diamond+Jackpot&font=raleway&bg=8b5a2b&textbg=4a2c1a"),
    ("Millionaire's Row", "millionaires-row", "jackpots", "HOT", 92.6, "https://placehold.co/400x500?text=Millionaires+Row&font=raleway&bg=4a2c1a&textbg=8b5a2b"),
    ("Golden Jackpot Wheel", "golden-jackpot-wheel", "jackpots", None, 93.5, "https://placehold.co/400x500?text=Golden+Jackpot&font=raleway&bg=8b5a2b&textbg=4a2c1a"),
    ("Super Jackpot Slots", "super-jackpot-slots", "jackpots", "NEW", 92.9, "https://placehold.co/400x500?text=Super+Jackpot&font=raleway&bg=4a2c1a&textbg=8b5a2b"),
    ("Vault Breaker", "vault-breaker", "jackpots", None, 93.1, "https://placehold.co/400x500?text=Vault+Breaker&font=raleway&bg=8b5a2b&textbg=4a2c1a"),
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

    for i, (name, slug, cat_slug, badge, rtp, image_url) in enumerate(GAMES):
        if Game.query.filter_by(slug=slug).first():
            continue
        db.session.add(Game(
            name=name,
            slug=slug,
            category_id=slug_to_cat[cat_slug].id,
            badge=badge,
            rtp_percent=rtp,
            image_url=image_url,
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
