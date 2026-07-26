# CyberShield SOC

Offline, Flask-based SOC dashboard with RBAC, secure sessions, alert and incident workflows, security logging, threat intelligence, vulnerability/asset inventory, audit trail, CSV exports, and PDF incident reports.

## Quick start

1. Install MySQL Community Edition and create a database/user:
   `CREATE DATABASE cybershield_soc CHARACTER SET utf8mb4;`
2. Copy `.env.example` to `.env` and set `DATABASE_URL` and a unique `SECRET_KEY`.
3. Create and activate a virtual environment; run `pip install -r requirements.txt`.
4. Seed: `flask --app run.py shell < database/seed.py` (PowerShell: `Get-Content database/seed.py | flask --app run.py shell`).
5. Start: `python run.py`, then visit `http://127.0.0.1:5000`.

Initial demo credentials: `admin` / `ChangeMe!2026`. Change immediately.

## Architecture and API

Blueprints: `auth` (identity), `soc` (operations), and `admin` (administration). Models are in `app/models.py`; reporting is isolated under `app/services`. Browser routes use server-rendered HTML and CSRF-protected forms. CSV/PDF endpoints: `/alerts/export` and `/incidents/<id>/pdf`.

## Deployment

On Ubuntu, install Python, MySQL, Nginx and system dependencies; deploy the project at `/opt/cybershield-soc`, use the supplied systemd service and Nginx virtual host in `deploy/`, enable both, and set `COOKIE_SECURE=true` behind HTTPS. Never use the development default secret in deployment.

## Security controls

Passwords are bcrypt hashes, forms have CSRF tokens, all database access uses SQLAlchemy parameterized queries, sessions are HttpOnly/SameSite, account lockout occurs after five failures, and sensitive operations generate audit records. Configure HTTPS and secure cookie mode in production.
