from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import current_app
import os

def generate_incident_pdf(incident):
    filename = f"incident-{incident.id}-{datetime.utcnow():%Y%m%d%H%M%S}.pdf"; path = os.path.join(current_app.config["REPORT_FOLDER"], filename)
    pdf = canvas.Canvas(path, pagesize=letter); pdf.setTitle(f"CyberShield Incident {incident.id}")
    y = 750
    for label, value in [("Incident", f"#{incident.id}: {incident.title}"),("Priority", incident.priority),("Status", incident.status),("Affected assets", incident.affected_assets or "N/A"),("Root cause", incident.root_cause or "N/A"),("Final report", incident.final_report or "N/A")]:
        pdf.drawString(50, y, f"{label}: {str(value)[:105]}"); y -= 35
    pdf.save(); return filename
