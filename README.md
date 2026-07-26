# Cyber Shield SOC

> A local-first Security Operations Center (SOC) dashboard built with Flask, MySQL, and open-source software.

CyberShield SOC is a dark-themed security operations platform for demonstrating and managing simulated security events. It provides secure authentication, role-based access control, alert and incident workflows, security logs, threat intelligence, vulnerability tracking, asset inventory, audit records, CSV exports, and PDF incident reports—without cloud services or paid APIs.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?logo=mysql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- Secure login, logout, password change, session timeout, CSRF protection, bcrypt password hashing, and five-attempt account lockout.
- Role-based access control for Super Admin, SOC Manager, Security Analyst, Incident Responder, and Auditor roles.
- Dashboard with alert, incident, vulnerability, asset, malware, and failed-login metrics.
- Alert creation, editing, deletion, filtering, search, and CSV export.
- Incident lifecycle management with investigation details, evidence upload, closure fields, and downloadable PDF reports.
- Searchable security log viewer, threat indicators, vulnerability tracking, and asset inventory.
- Administrative user creation, enable/disable controls, and audit trail visibility.
- Simulated SOC data for ransomware, phishing, failed logins, brute-force attempts, firewall events, assets, CVEs, and indicators of compromise.
- Local PDF reporting with ReportLab and deployment templates for Gunicorn and Nginx.

## 🛠️ Technology stack

| Layer | Technology |
| --- | --- |
| Backend | Python, Flask |
| Database | MySQL Community Edition |
| ORM | SQLAlchemy |
| Authentication | Flask-Login, Flask-Bcrypt |
| Forms & CSRF | Flask-WTF |
| Configuration | python-dotenv |
| Reporting | ReportLab |
| Production server | Gunicorn + Nginx |
| Frontend | HTML5, CSS3, Jinja templates |

## 🚀 Quick start (Laragon on Windows)

### 1. Start MySQL

Open Laragon and click **Start All**. Open **Database** (HeidiSQL) and run:

``sql
CREATE DATABASE cybershield_soc
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
2. Configure environment variables
Copy .env.example to .env:
SECRET_KEY=replace-with-a-long-random-secret
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/cybershield_soc
SESSION_TIMEOUT_MINUTES=30
COOKIE_SECURE=false
If your MySQL root account has a password, include it in DATABASE_URL.
3. Install dependencies
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
4. Load sample SOC data
$env:PYTHONPATH='.'
.\.venv\Scripts\python.exe database\seed.py
5. Run the dashboard
.\.venv\Scripts\python.exe run.py
Open http://127.0.0.1:5000.``


## 📁 Project structure

CyberShield-SOC/
├── app/
│   ├── routes/             # Authentication, SOC, and admin blueprints
│   ├── services/           # PDF reporting service
│   ├── static/             # Stylesheets and browser assets
│   ├── templates/          # Jinja pages
│   ├── forms.py            # Flask-WTF input validation
│   ├── models.py           # SQLAlchemy database models
│   └── security.py         # RBAC and audit helpers
├── database/
│   ├── schema.md
│   └── seed.py             # Demonstration dataset
├── deploy/                 # Nginx and systemd examples
├── docs/                   # Installation, architecture, API, deployment docs
├── uploads/                # Local incident evidence uploads
├── reports/                # Generated PDF reports
├── requirements.txt
├── run.py
└── wsgi.py

## 👥 Roles and access
Role	Intended Access
Super Admin	Full system administration and all SOC actions
SOC Manager	Alert/incident management and administration controls
Security Analyst	Alert and incident investigation workflows
Incident Responder	Incident response workflows
Auditor	Read-only operational visibility

## 🔐 Security controls
Passwords stored with bcrypt hashes.
CSRF protection for state-changing forms.
SQLAlchemy ORM parameterizes database queries.
HTTP-only and SameSite session cookies.
Account lockout for 30 minutes after five failed sign-in attempts.
Input validation through Flask-WTF and WTForms.
Role and permission checks on protected routes.
Audit log entries for sensitive actions.

## 🧭 Operational routes
Route	Purpose
/dashboard	SOC security overview
/alerts	Alert management and CSV export
/incidents	Incident workflow and PDF reports
/logs	Security log viewer
/threat-intelligence	Indicators of compromise
/vulnerabilities	CVE and remediation tracking
/assets	Asset inventory
/admin/	Super Admin console

## 🐧 Production deployment (Ubuntu)
Provision MySQL and an application-specific database user.
Create a Python virtual environment and install dependencies.
Set production .env values, including a unique SECRET_KEY.
Set COOKIE_SECURE=true behind HTTPS.
Run Gunicorn using wsgi:app.
Configure Nginx using the examples in deploy/.

## 👨‍💻 Author

**Rishi Mohan Jha**

## ⚠️ Disclaimer
CyberShield SOC is an educational and demonstration application using simulated security telemetry. It is not a replacement for a fully hardened commercial SOC or SIEM platform. Review security controls, enable HTTPS, rotate secrets, and test access controls before real-world use.
