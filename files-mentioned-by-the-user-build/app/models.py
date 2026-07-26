from datetime import datetime
from flask_login import UserMixin
from app import db, bcrypt

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    permissions = db.Column(db.String(500), default="")

class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    failed_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    role = db.relationship("Role"); department = db.relationship("Department")
    def set_password(self, password): self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    def check_password(self, password): return bcrypt.check_password_hash(self.password_hash, password)
    def has_permission(self, permission): return self.role and ("*" in self.role.permissions or permission in self.role.permissions.split(","))

class Asset(TimestampMixin, db.Model):
    __tablename__ = "assets"
    id = db.Column(db.Integer, primary_key=True); name = db.Column(db.String(120), nullable=False, unique=True)
    asset_type = db.Column(db.String(50), nullable=False); owner = db.Column(db.String(100)); department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    operating_system = db.Column(db.String(100)); criticality = db.Column(db.String(20), default="Medium"); risk_level = db.Column(db.String(20), default="Low")
    last_scan = db.Column(db.DateTime); ip_address = db.Column(db.String(45)); department = db.relationship("Department")

class Alert(TimestampMixin, db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True); title = db.Column(db.String(200), nullable=False); description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False, default="Medium"); status = db.Column(db.String(30), nullable=False, default="Open")
    category = db.Column(db.String(80)); source = db.Column(db.String(100)); notes = db.Column(db.Text)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey("users.id")); assigned_to = db.relationship("User")

class Incident(TimestampMixin, db.Model):
    __tablename__ = "incidents"
    id = db.Column(db.Integer, primary_key=True); title = db.Column(db.String(200), nullable=False); priority = db.Column(db.String(20), default="Medium")
    status = db.Column(db.String(30), default="Open"); affected_assets = db.Column(db.Text); timeline = db.Column(db.Text); investigation_notes = db.Column(db.Text)
    evidence_path = db.Column(db.String(255)); recovery_steps = db.Column(db.Text); root_cause = db.Column(db.Text); final_report = db.Column(db.Text)
    closed_at = db.Column(db.DateTime)

class Vulnerability(TimestampMixin, db.Model):
    __tablename__ = "vulnerabilities"
    id = db.Column(db.Integer, primary_key=True); cve_id = db.Column(db.String(32), unique=True, nullable=False); cvss_score = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text); risk_level = db.Column(db.String(20)); patch_status = db.Column(db.String(30), default="Pending")
    assigned_engineer = db.Column(db.String(100)); remediation_deadline = db.Column(db.Date); status = db.Column(db.String(30), default="Open")
    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id")); asset = db.relationship("Asset")

class SecurityLog(TimestampMixin, db.Model):
    __tablename__ = "security_logs"
    id = db.Column(db.Integer, primary_key=True); log_type = db.Column(db.String(40), nullable=False); severity = db.Column(db.String(20), default="Info")
    source = db.Column(db.String(100)); message = db.Column(db.Text, nullable=False); event_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True); user_id = db.Column(db.Integer, db.ForeignKey("users.id")); action = db.Column(db.String(100), nullable=False)
    entity = db.Column(db.String(100)); details = db.Column(db.Text); ip_address = db.Column(db.String(45)); created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship("User")

class LoginLog(db.Model):
    __tablename__ = "login_logs"
    id = db.Column(db.Integer, primary_key=True); user_id = db.Column(db.Integer, db.ForeignKey("users.id")); username = db.Column(db.String(64))
    ip_address = db.Column(db.String(45)); successful = db.Column(db.Boolean, nullable=False); created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class ThreatFeed(TimestampMixin, db.Model):
    __tablename__ = "threat_feeds"
    id = db.Column(db.Integer, primary_key=True); name = db.Column(db.String(120), nullable=False); source = db.Column(db.String(120)); imported_at = db.Column(db.DateTime, default=datetime.utcnow)

class IOC(TimestampMixin, db.Model):
    __tablename__ = "ioc"
    id = db.Column(db.Integer, primary_key=True); indicator = db.Column(db.String(255), unique=True, nullable=False); indicator_type = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(80)); risk_score = db.Column(db.Integer, default=50); status = db.Column(db.String(20), default="Active"); feed_id = db.Column(db.Integer, db.ForeignKey("threat_feeds.id"))
    feed = db.relationship("ThreatFeed")

class Report(TimestampMixin, db.Model):
    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True); report_type = db.Column(db.String(50), nullable=False); filename = db.Column(db.String(255), nullable=False); created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))

class Setting(TimestampMixin, db.Model):
    __tablename__ = "settings"
    id = db.Column(db.Integer, primary_key=True); key = db.Column(db.String(100), unique=True, nullable=False); value = db.Column(db.Text, nullable=False)

class Notification(TimestampMixin, db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True); user_id = db.Column(db.Integer, db.ForeignKey("users.id")); message = db.Column(db.String(255), nullable=False); read = db.Column(db.Boolean, default=False)
