# API / operational endpoints

The application is server-rendered and does not expose unauthenticated JSON APIs. Operational endpoints require Flask-Login sessions and role permissions:

- `GET /alerts/export` exports alerts as CSV.
- `GET /incidents/<id>/pdf` creates and downloads an incident PDF.
- `POST /alerts/<id>/delete` deletes an alert (manager/admin only).
- `POST /admin/users` creates a user (administrator only).

All POST requests require a valid CSRF token.
