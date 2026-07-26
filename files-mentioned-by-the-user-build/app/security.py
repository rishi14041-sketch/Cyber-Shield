from functools import wraps
from flask import abort, request
from flask_login import current_user
from app import db
from app.models import AuditLog

def permission_required(permission):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated: return abort(401)
            if not current_user.has_permission(permission): return abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator
def audit(action, entity="", details=""):
    if current_user.is_authenticated:
        db.session.add(AuditLog(user_id=current_user.id, action=action, entity=entity, details=details[:1000], ip_address=request.remote_addr))
