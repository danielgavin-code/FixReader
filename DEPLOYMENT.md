# FIXReader Deployment Guide

## Requirements

- Python 3.10+
- pip packages: `flask`, `gunicorn` (production), `pytest` (tests)

Install:
```
pip install flask gunicorn
pip install pytest  # dev/test only
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CANONICAL_HOST` | No | `fixreader.net` | Hostname used in `robots.txt` Sitemap URL and `sitemap.xml` `<loc>` entries. Set to the production domain. |
| `ENABLE_THEME_ADMIN` | No | _(unset)_ | Set to `true` to enable the `/themes-admin` UI. **Must be unset or absent in production.** |

No secret key or database credentials are required.

---

## Running

### Development

```
flask --app app run --debug
```

Or directly:

```
python app.py
```

The `debug=True` inside `if __name__ == '__main__'` is development-only. Flask's built-in server is **not** suitable for production.

### Production

```
gunicorn app:app --workers 2 --bind 0.0.0.0:8000
```

Adjust `--workers` to match your CPU count. Serve behind a reverse proxy (nginx, Caddy, or your platform's load balancer) that handles TLS termination and HTTPS redirection.

---

## HTTPS / Canonical URL

HTTPS enforcement and `www` → apex (or apex → `www`) redirects should be handled at the proxy layer, **not** in the Flask app. Configure your reverse proxy or platform to:

1. Redirect all HTTP traffic to HTTPS (301).
2. Redirect `www.fixreader.net` → `fixreader.net` (or vice versa, consistently).

Doing redirects in Flask risks redirect loops when the proxy forwards `X-Forwarded-Proto`.

---

## Rate Limiting

The `/decode` POST endpoint, Tag Validator (`/tools/tag-validator`), and Message Builder (`/tools/message-builder`) accept user-submitted input. Rate limiting should be applied at the reverse proxy or CDN layer.

If app-level rate limiting is needed, add `flask-limiter` and configure it with a Redis or memcached backend. The app will return 429 for exceeded limits.

---

## Request Size Limit

Requests exceeding 2 MB are rejected with a 413 response and a user-friendly error page. No stack trace or internal details are exposed.

---

## Logging

The app uses Flask's default Werkzeug request logger (route, status, size). FIX message content submitted to `/decode` is **not** logged — only the route, response status, and response size appear in access logs.

For structured logging in production, configure gunicorn's `--access-logfile` and `--error-logfile`, or pipe stdout/stderr to your log aggregator.

---

## Pre-launch Checklist

Run tests:

```
pytest
```

Confirm all pass before deploying.

### Verify production settings

```
# Debug mode is off (module-level, not __main__):
python -c "import app; assert not app.app.debug, 'DEBUG IS ON'"

# Theme admin is disabled:
curl -s -o /dev/null -w "%{http_code}" https://fixreader.net/themes-admin
# Expected: 404

# robots.txt is reachable and references sitemap:
curl -s https://fixreader.net/robots.txt

# sitemap.xml is valid XML with HTTPS URLs:
curl -s https://fixreader.net/sitemap.xml

# Security headers present:
curl -sI https://fixreader.net/ | grep -E 'X-Content-Type|X-Frame|Content-Security'

# Decoder is functional:
curl -s -X POST https://fixreader.net/decode \
  -d 'fix_message=8=FIX.4.2|9=49|35=D|49=CLIENT|56=BROKER|34=1|52=20240315-09:30:00|10=123|' \
  | python -m json.tool
# Expected: {"status": "ok", "fields": [...], "summary": "..."}
```

---

## Rollback

1. `git log --oneline -10` — identify the last good commit.
2. `git checkout <commit>` on the server, or redeploy the previous release artifact.
3. Restart gunicorn: `kill -HUP <pid>` or restart the process supervisor.
4. Re-run the pre-launch checklist above.

---

## Theme Management

Themes are stored in `fixreader_data/themes.json`. The active theme is written to `fixreader_active_theme.json`.

To set a theme manually:

```
python fixreader_Themes.py --set default
python fixreader_Themes.py --today          # auto-select by date
python fixreader_Themes.py --list           # show all themes
```

The theme admin UI (`/themes-admin`) must remain disabled in production unless explicitly needed. Verify with `curl -s -o /dev/null -w "%{http_code}" .../themes-admin` → `404`.
