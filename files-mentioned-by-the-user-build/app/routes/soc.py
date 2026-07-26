import csv, io, os
from datetime import datetime
from flask import Blueprint, Response, abort, flash, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.forms import AlertForm, IncidentForm
from app.models import Alert, Asset, Incident, IOC, SecurityLog, Vulnerability
from app.security import audit, permission_required
from app.services.reporting import generate_incident_pdf

soc_bp = Blueprint("soc", __name__)
def page(query, model): return query.paginate(page=request.args.get("page", 1, type=int), per_page=20, error_out=False)
@soc_bp.route("/dashboard")
@login_required
def dashboard():
    stats = {"alerts": Alert.query.count(), "critical": Alert.query.filter_by(severity="Critical").count(), "active_incidents": Incident.query.filter(Incident.status != "Closed").count(), "resolved": Incident.query.filter_by(status="Closed").count(), "vulns": Vulnerability.query.filter(Vulnerability.status != "Closed").count(), "assets": Asset.query.filter(Asset.risk_level.in_(["High", "Critical"])).count(), "failed": SecurityLog.query.filter(SecurityLog.message.ilike("%failed%" )).count(), "malware": Alert.query.filter(Alert.category.ilike("%malware%")).count()}
    return render_template("dashboard.html", stats=stats, latest=Alert.query.order_by(Alert.created_at.desc()).limit(8).all())
@soc_bp.route("/alerts")
@login_required
def alerts():
    q = Alert.query
    if term := request.args.get("q"): q = q.filter(Alert.title.ilike(f"%{term}%"))
    if severity := request.args.get("severity"): q = q.filter_by(severity=severity)
    if status := request.args.get("status"): q = q.filter_by(status=status)
    return render_template("alerts.html", alerts=page(q.order_by(Alert.created_at.desc()), Alert), title="Alert management")
@soc_bp.route("/alerts/new", methods=["GET", "POST"])
@login_required
@permission_required("alerts.write")
def alert_new(): return alert_edit(None)
@soc_bp.route("/alerts/<int:alert_id>/edit", methods=["GET", "POST"])
@login_required
@permission_required("alerts.write")
def alert_edit(alert_id):
    alert = db.session.get(Alert, alert_id) if alert_id else Alert()
    if not alert: abort(404)
    form = AlertForm(obj=alert)
    if form.validate_on_submit():
        form.populate_obj(alert); db.session.add(alert); audit("Create Alert" if not alert_id else "Update Alert", "Alert", alert.title); db.session.commit(); flash("Alert saved.", "success"); return redirect(url_for("soc.alerts"))
    return render_template("form.html", form=form, title="Create alert" if not alert_id else f"Edit alert #{alert.id}")
@soc_bp.route("/alerts/<int:alert_id>/delete", methods=["POST"])
@login_required
@permission_required("alerts.delete")
def alert_delete(alert_id):
    alert = db.session.get(Alert, alert_id) or abort(404); audit("Delete Alert", "Alert", alert.title); db.session.delete(alert); db.session.commit(); flash("Alert deleted.", "success"); return redirect(url_for("soc.alerts"))
@soc_bp.route("/alerts/export")
@login_required
def alerts_export():
    out = io.StringIO(); writer = csv.writer(out); writer.writerow(["ID","Title","Severity","Status","Category","Source","Created"])
    for a in Alert.query.order_by(Alert.created_at.desc()): writer.writerow([a.id,a.title,a.severity,a.status,a.category,a.source,a.created_at])
    return Response(out.getvalue(), mimetype="text/csv", headers={"Content-Disposition":"attachment; filename=alerts.csv"})
@soc_bp.route("/incidents")
@login_required
def incidents(): return render_template("incidents.html", incidents=page(Incident.query.order_by(Incident.created_at.desc()), Incident), title="Incident management")
@soc_bp.route("/incidents/new", methods=["GET", "POST"])
@login_required
@permission_required("incidents.write")
def incident_new(): return incident_edit(None)
@soc_bp.route("/incidents/<int:incident_id>/edit", methods=["GET", "POST"])
@login_required
@permission_required("incidents.write")
def incident_edit(incident_id):
    incident = db.session.get(Incident, incident_id) if incident_id else Incident()
    if not incident: abort(404)
    form = IncidentForm(obj=incident)
    if form.validate_on_submit():
        form.populate_obj(incident)
        if request.files.get("evidence") and request.files["evidence"].filename:
            name = secure_filename(request.files["evidence"].filename); filename = f"incident-{incident.id or 'new'}-{name}"; request.files["evidence"].save(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", filename)); incident.evidence_path = filename
        if incident.status == "Closed": incident.closed_at = datetime.utcnow()
        db.session.add(incident); audit("Update Incident" if incident_id else "Create Incident", "Incident", incident.title); db.session.commit(); flash("Incident saved.", "success"); return redirect(url_for("soc.incidents"))
    return render_template("form.html", form=form, title="Create incident" if not incident_id else f"Edit incident #{incident.id}", multipart=True)
@soc_bp.route("/incidents/<int:incident_id>/pdf")
@login_required
def incident_pdf(incident_id):
    incident = db.session.get(Incident, incident_id) or abort(404); filename = generate_incident_pdf(incident); audit("Generate Incident Report", "Incident", incident.title); db.session.commit(); return send_from_directory(os.path.join(os.path.dirname(__file__), "..", "..", "reports"), filename, as_attachment=True)
@soc_bp.route("/logs")
@login_required
def logs():
    q=SecurityLog.query
    if term := request.args.get("q"): q=q.filter(SecurityLog.message.ilike(f"%{term}%"))
    if sev := request.args.get("severity"): q=q.filter_by(severity=sev)
    return render_template("logs.html", logs=page(q.order_by(SecurityLog.event_time.desc()), SecurityLog), title="Security log viewer")
@soc_bp.route("/threat-intelligence")
@login_required
def threats(): return render_template("threats.html", iocs=page(IOC.query.order_by(IOC.risk_score.desc()), IOC), title="Threat intelligence")
@soc_bp.route("/vulnerabilities")
@login_required
def vulnerabilities(): return render_template("vulnerabilities.html", vulnerabilities=page(Vulnerability.query.order_by(Vulnerability.cvss_score.desc()), Vulnerability), title="Vulnerability management")
@soc_bp.route("/assets")
@login_required
def assets(): return render_template("assets.html", assets=page(Asset.query.order_by(Asset.risk_level.desc()), Asset), title="Asset inventory")
