# CyberShield SOC database schema

The SQLAlchemy models implement normalized MySQL tables with foreign keys for users→roles/departments, assets→departments, alerts→users, vulnerabilities→assets, IOC→threat_feeds, and audit/login/report records→users. Apply with `flask db init`, `flask db migrate`, and `flask db upgrade`, or run the offline seed script for a first local environment.
