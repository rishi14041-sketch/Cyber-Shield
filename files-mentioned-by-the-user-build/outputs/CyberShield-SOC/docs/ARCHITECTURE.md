# Project architecture

`app/__init__.py` owns configuration and extensions. Blueprints split authentication, SOC operations, and administration. SQLAlchemy models provide persistence; forms validate all browser mutations; `security.py` centralizes RBAC/audit functions; and `services/reporting.py` creates local PDF reports. Static assets and Jinja templates comprise the responsive browser console.
