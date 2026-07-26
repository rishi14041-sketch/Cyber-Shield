# Ubuntu deployment guide

Use a dedicated non-login service account, a virtual environment, MySQL TLS where available, and an HTTPS-terminating Nginx server. Copy `deploy/cybershield.service` and `deploy/nginx.conf`, update paths/domain, set `COOKIE_SECURE=true`, then run `systemctl daemon-reload`, enable the service, and reload Nginx. Keep `.env`, uploads, reports, and database backups outside source control.
