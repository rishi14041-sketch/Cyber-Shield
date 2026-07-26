from datetime import datetime, timedelta
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import db
from app.forms import LoginForm, PasswordForm
from app.models import LoginLog, User
from app.security import audit

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: return redirect(url_for("soc.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first(); now = datetime.utcnow()
        valid = user and user.active and (not user.locked_until or user.locked_until <= now) and user.check_password(form.password.data)
        db.session.add(LoginLog(user_id=user.id if user else None, username=form.username.data, ip_address=request.remote_addr, successful=bool(valid)))
        if valid:
            user.failed_attempts = 0; user.last_login = now; login_user(user); audit("Login", "User", user.username); db.session.commit()
            return redirect(request.args.get("next") or url_for("soc.dashboard"))
        if user:
            user.failed_attempts += 1
            if user.failed_attempts >= 5: user.locked_until = now + timedelta(minutes=30)
        db.session.commit(); flash("Invalid credentials or account temporarily locked.", "danger")
    return render_template("login.html", form=form)
@auth_bp.route("/logout")
@login_required
def logout():
    audit("Logout", "User", current_user.username); db.session.commit(); logout_user(); flash("You have been signed out.", "info"); return redirect(url_for("auth.login"))
@auth_bp.route("/password", methods=["GET", "POST"])
@login_required
def password():
    form = PasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data): flash("Current password is incorrect.", "danger")
        else:
            current_user.set_password(form.password.data); audit("Change Password", "User", current_user.username); db.session.commit(); flash("Password updated.", "success"); return redirect(url_for("soc.dashboard"))
    return render_template("form.html", form=form, title="Change password")
@auth_bp.route("/forgot", methods=["GET", "POST"])
def forgot():
    # Offline-safe workflow: managers reset accounts through Admin > Users; no external mail service is required.
    if request.method == "POST": flash("If the account exists, your SOC manager can reset it through the offline administration console.", "info"); return redirect(url_for("auth.login"))
    return render_template("forgot.html")
