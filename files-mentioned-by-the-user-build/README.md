# CyberShield SOC

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
- Alert creation, editing, deletion, filtering, search, assignment-ready fields, and CSV export.
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

## Screenshots

Run the application locally and add screenshots to a `docs/screenshots/` directory if you publish the project. Suggested screenshots:

- Login page
- Security overview dashboard
- Alert management table
- Incident management workflow

## 🚀 Quick start (Laragon on Windows)

### 1. Start MySQL

Open Laragon and click **Start All**. Then open **Database** (HeidiSQL) and create the database:

```sql
CREATE DATABASE cybershield_soc
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

### 2. Configure the application

Copy `.env.example` to `.env` and set the connection string. Laragon commonly uses `root` with an empty password:

```env
SECRET_KEY=replace-with-a-long-random-secret
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/cybershield_soc
SESSION_TIMEOUT_MINUTES=30
COOKIE_SECURE=false
```

If your MySQL root account has a password, include it in `DATABASE_URL`.

### 3. Install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Load demonstration data

```powershell
$env:PYTHONPATH='.'
.\.venv\Scripts\python.exe database\seed.py
```

### 5. Start the dashboard

```powershell
.\.venv\Scripts\python.exe run.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Demo account

| Username | Password | Role |
| --- | --- | --- |
| `admin` | `ChangeMe!2026` | Super Admin |

Change the demo password immediately after first sign-in at `/auth/password`.

## 📁 Project structure

```text
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
```

## 👥 Roles and access

| Role | Intended access |
| --- | --- |
| Super Admin | Full system administration and all SOC actions |
| SOC Manager | Alert/incident management and administration controls |
| Security Analyst | Alert and incident investigation workflows |
| Incident Responder | Incident response workflows |
| Auditor | Read-only operational visibility |

## 🔐 Security controls

- Passwords stored with bcrypt hashes.
- CSRF protection for all state-changing forms.
- SQLAlchemy ORM parameterizes database queries.
- HTTP-only and SameSite session cookies.
- Account lockout for 30 minutes after five failed sign-in attempts.
- Input validation through Flask-WTF and WTForms.
- Role/permission checks on protected routes.
- Audit log entries for sensitive actions such as login, logout, alert changes, password changes, and user management.

## 🧭 Operational routes

| Route | Purpose |
| --- | --- |
| `/dashboard` | SOC security overview |
| `/alerts` | Alert management and CSV export |
| `/incidents` | Incident workflow and PDF reports |
| `/logs` | Security log viewer |
| `/threat-intelligence` | Indicators of compromise |
| `/vulnerabilities` | CVE and remediation tracking |
| `/assets` | Asset inventory |
| `/admin/` | Super Admin console |

## 🐧 Production deployment (Ubuntu)

1. Provision a MySQL database and an application-specific MySQL user.
2. Create a Python virtual environment and install `requirements.txt`.
3. Set production values in `.env`, including a unique `SECRET_KEY` and `COOKIE_SECURE=true`.
4. Configure Gunicorn using `wsgi:app`.
5. Use the examples in `deploy/cybershield.service` and `deploy/nginx.conf` as a starting point.
6. Terminate TLS at Nginx and restrict filesystem/database permissions to the service account.

See [deployment documentation](docs/DEPLOYMENT.md) for more detail.

## 📚 Documentation

- [Installation guide](docs/INSTALLATION.md)
- [Project architecture](docs/ARCHITECTURE.md)
- [Operational API notes](docs/API.md)
- [Database schema notes](database/schema.md)
- [Deployment guide](docs/DEPLOYMENT.md)

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make focused changes and test locally.
4. Submit a pull request with a clear description.

## 📄 License

This project is released under the MIT License. Add a `LICENSE` file before publishing if one is not already present.

## 👨‍💻 Author

**Rishi Jha**

CyberShield SOC was created as an enterprise-style cybersecurity dashboard project using Flask, MySQL, and free, open-source technologies.

## ⚠️ Disclaimer

CyberShield SOC is an educational and demonstration application that uses simulated security telemetry. It is not a replacement for a fully hardened commercial SOC/SIEM deployment. Perform a security review, use HTTPS, rotate secrets, implement backups, and test access controls before any real-world use.
