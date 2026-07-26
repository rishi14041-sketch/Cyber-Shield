# Installation guide

Install MySQL Community Edition, create `cybershield_soc`, and grant a restricted application user only the privileges required on that schema. Copy `.env.example` to `.env`, use a cryptographically random `SECRET_KEY`, then install `requirements.txt` inside a Python virtual environment. Run the seed command in the root README to create the normalized tables and demonstration data.

For migrations after model changes, use Flask-Migrate: `flask --app run.py db init`, `flask --app run.py db migrate -m "description"`, and `flask --app run.py db upgrade`.
