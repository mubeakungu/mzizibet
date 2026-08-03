from flask import Flask, redirect, url_for
from config import config
from app.extensions import db, login_manager, migrate, bcrypt


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from app.models.user import User

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

    @app.context_processor
    def inject_globals():
        return {"site_name": "Mzizibet"}

    @app.route("/")
    def index():
        return redirect(url_for("sports.lobby"))

    # Local dev convenience: auto-create SQLite tables on startup so the
    # app runs with zero setup — no `flask db upgrade` needed just to
    # browse the site. Production (Postgres/Render) should still use
    # proper migrations via Flask-Migrate.
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        from app.models import wallet, casino, sports  # noqa: F401

        with app.app_context():
            db.create_all()

    return app
