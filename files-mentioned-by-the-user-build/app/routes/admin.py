from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app import db
from app.models import AuditLog, Role, User
from app.security import audit, permission_required
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
@admin_bp.route("/")
@login_required
@permission_required("admin")
def index(): return render_template("admin.html", users=User.query.order_by(User.username).all(), roles=Role.query.order_by(Role.name).all(), audit_logs=AuditLog.query.order_by(AuditLog.created_at.desc()).limit(50).all(), title="Administration")
@admin_bp.route("/users", methods=["POST"])
@login_required
@permission_required("admin")
def create_user():
    username=request.form.get("username", "").strip(); email=request.form.get("email", "").strip().lower(); password=request.form.get("password", ""); role=Role.query.get(request.form.get("role_id", type=int))
    if len(username) < 3 or "@" not in email or len(password) < 12 or not role: flash("Provide a unique username, valid email, role, and a 12-character password.", "danger")
    elif User.query.filter((User.username==username)|(User.email==email)).first(): flash("Username or email is already in use.", "danger")
    else:
        user=User(username=username, email=email, role=role); user.set_password(password); db.session.add(user); audit("Create User", "User", username); db.session.commit(); flash("User created.", "success")
    return redirect(url_for("admin.index"))
@admin_bp.route("/users/<int:user_id>/toggle", methods=["POST"])
@login_required
@permission_required("admin")
def toggle_user(user_id):
    user=db.session.get(User,user_id); user.active=not user.active; audit("Disable User" if not user.active else "Enable User", "User", user.username); db.session.commit(); flash("User status updated.", "success"); return redirect(url_for("admin.index"))
