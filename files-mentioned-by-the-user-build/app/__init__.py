import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "development-only-change-before-deployment"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "mysql+pymysql://root:@127.0.0.1/cybershield_soc"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))),
        SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        MAX_CONTENT_LENGTH=10 * 1024 * 1024,
        UPLOAD_FOLDER=os.path.join(app.root_path, "..", "uploads"),
        REPORT_FOLDER=os.path.join(app.root_path, "..", "reports"),
    )
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["REPORT_FOLDER"], exist_ok=True)
    db.init_app(app); bcrypt.init_app(app); csrf.init_app(app); migrate.init_app(app, db)
    login_manager.init_app(app); login_manager.login_view = "auth.login"; login_manager.login_message_category = "warning"
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id): return db.session.get(User, int(user_id))
    @app.context_processor
    def globals_(): return {"app_name": "CyberShield SOC"}
    from app.routes.auth import auth_bp
    from app.routes.soc import soc_bp
    from app.routes.admin import admin_bp
    app.register_blueprint(auth_bp); app.register_blueprint(soc_bp); app.register_blueprint(admin_bp)
    @app.route("/")
    def index(): return redirect(url_for("soc.dashboard"))
    return app
