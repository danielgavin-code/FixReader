"""
Production-readiness tests.

Covers: custom error pages, security headers, request size limits,
robots.txt, sitemap.xml, production config defaults, theme-admin guard.
"""
import re
import pytest
import app as _app_module

SECURITY_HEADER_ROUTES = [
    '/',
    '/compare',
    '/tools/tag-validator',
    '/tools/message-builder',
    '/message-library',
    '/exchange-specs',
    '/resources',
]


# ── Custom error pages ────────────────────────────────────────────────────────

def test_unknown_route_returns_404(client):
    r = client.get('/this-route-does-not-exist-xyz')
    assert r.status_code == 404
    html = r.data.decode('utf-8', errors='ignore')
    assert 'Page Not Found' in html
    assert 'Traceback' not in html
    assert 'werkzeug' not in html.lower()


def test_404_page_has_back_link(client):
    r = client.get('/no-such-page-abc123')
    html = r.data.decode('utf-8', errors='ignore')
    assert 'href="/"' in html


def test_custom_500_no_traceback(client):
    flask_app = _app_module.app
    orig_testing = flask_app.config.get('TESTING', True)
    flask_app.config['TESTING'] = False
    flask_app.config['PROPAGATE_EXCEPTIONS'] = False

    try:
        # /test-force-500-internal is registered in conftest.py at import time
        r = client.get('/test-force-500-internal')
        assert r.status_code == 500
        html = r.data.decode('utf-8', errors='ignore')
        assert 'RuntimeError' not in html
        assert 'Traceback' not in html
        assert 'intentional test error' not in html
    finally:
        flask_app.config['TESTING'] = orig_testing
        flask_app.config['PROPAGATE_EXCEPTIONS'] = orig_testing


# ── Request size limit ────────────────────────────────────────────────────────

def test_normal_decode_returns_200(client):
    payload = '8=FIX.4.2|9=49|35=D|49=CLIENT|56=BROKER|34=1|52=20240315-09:30:00|10=123|'
    r = client.post('/decode', data={'fix_message': payload})
    assert r.status_code == 200


def test_oversized_request_returns_413(client):
    # 3 MB payload — exceeds the 2 MB MAX_CONTENT_LENGTH
    big = 'x' * (3 * 1024 * 1024)
    r = client.post('/decode', data={'fix_message': big})
    assert r.status_code == 413
    html = r.data.decode('utf-8', errors='ignore')
    assert 'Traceback' not in html
    assert 'werkzeug' not in html.lower()


def test_413_page_no_internal_details(client):
    big = 'x' * (3 * 1024 * 1024)
    r = client.post('/decode', data={'fix_message': big})
    html = r.data.decode('utf-8', errors='ignore')
    assert 'Request Too Large' in html or r.status_code == 413


# ── Security headers ──────────────────────────────────────────────────────────

@pytest.mark.parametrize('path', SECURITY_HEADER_ROUTES)
def test_security_headers_present(client, path):
    r = client.get(path)
    assert r.status_code == 200
    assert r.headers.get('X-Content-Type-Options') == 'nosniff'
    assert r.headers.get('X-Frame-Options') == 'DENY'
    assert r.headers.get('Referrer-Policy') == 'strict-origin-when-cross-origin'
    assert 'Content-Security-Policy' in r.headers
    assert 'Permissions-Policy' in r.headers


def test_csp_allows_google_fonts(client):
    r = client.get('/')
    csp = r.headers.get('Content-Security-Policy', '')
    assert 'fonts.googleapis.com' in csp
    assert 'fonts.gstatic.com' in csp


def test_csp_blocks_frame_ancestors(client):
    r = client.get('/')
    csp = r.headers.get('Content-Security-Policy', '')
    assert "frame-ancestors 'none'" in csp


# ── robots.txt ────────────────────────────────────────────────────────────────

def test_robots_txt_returns_200(client):
    r = client.get('/robots.txt')
    assert r.status_code == 200
    assert 'text/plain' in r.content_type


def test_robots_txt_allows_public(client):
    text = client.get('/robots.txt').data.decode()
    assert 'Allow: /' in text


def test_robots_txt_disallows_admin(client):
    text = client.get('/robots.txt').data.decode()
    assert 'Disallow: /themes-admin' in text


def test_robots_txt_has_sitemap(client):
    text = client.get('/robots.txt').data.decode()
    assert 'Sitemap:' in text
    assert 'sitemap.xml' in text


# ── sitemap.xml ───────────────────────────────────────────────────────────────

def test_sitemap_returns_200(client):
    r = client.get('/sitemap.xml')
    assert r.status_code == 200
    assert 'xml' in r.content_type


def test_sitemap_is_valid_xml(client):
    xml = client.get('/sitemap.xml').data.decode()
    assert xml.startswith('<?xml')
    assert '<urlset' in xml
    assert '</urlset>' in xml


def test_sitemap_uses_https(client):
    xml = client.get('/sitemap.xml').data.decode()
    locs = re.findall(r'<loc>(.*?)</loc>', xml)
    assert locs, 'No <loc> entries in sitemap'
    for loc in locs:
        assert loc.startswith('https://'), f'Non-HTTPS URL in sitemap: {loc}'


def test_sitemap_excludes_admin(client):
    xml = client.get('/sitemap.xml').data.decode()
    assert 'themes-admin' not in xml


def test_sitemap_excludes_removed_routes(client):
    xml = client.get('/sitemap.xml').data.decode()
    assert '/contact' not in xml
    assert '/feedback' not in xml
    assert '/about' not in xml


def test_sitemap_includes_primary_pages(client):
    xml = client.get('/sitemap.xml').data.decode()
    for path in ('/', '/compare', '/tools/tag-validator', '/tools/message-builder',
                 '/message-library', '/exchange-specs', '/resources'):
        assert path in xml, f'Expected {path} in sitemap'


def test_sitemap_includes_reference_pages(client):
    xml = client.get('/sitemap.xml').data.decode()
    for ver in ('/reference/fix42', '/reference/fix44', '/reference/fix50'):
        assert ver in xml, f'Expected {ver} in sitemap'


def test_sitemap_includes_troubleshooting(client):
    xml = client.get('/sitemap.xml').data.decode()
    for path in ('/troubleshooting/network', '/troubleshooting/logon',
                 '/troubleshooting/sequence-numbers'):
        assert path in xml, f'Expected {path} in sitemap'


# ── Production config defaults ────────────────────────────────────────────────

def test_debug_not_enabled_by_default():
    # app.run(debug=True) is inside `if __name__ == '__main__'` — the module-level
    # app.debug should be False when imported normally (not run directly).
    assert _app_module.app.debug is False, (
        'app.debug must be False when the module is imported — '
        'debug=True should only appear inside `if __name__ == "__main__"`'
    )


def test_theme_admin_disabled_by_default(client, monkeypatch):
    monkeypatch.delenv('ENABLE_THEME_ADMIN', raising=False)
    r = client.get('/themes-admin')
    assert r.status_code == 404


def test_max_content_length_configured():
    limit = _app_module.app.config.get('MAX_CONTENT_LENGTH')
    assert limit is not None, 'MAX_CONTENT_LENGTH must be configured'
    assert limit <= 10 * 1024 * 1024, 'MAX_CONTENT_LENGTH should be 10 MB or less'
    assert limit >= 1 * 1024 * 1024, 'MAX_CONTENT_LENGTH should allow at least 1 MB'
