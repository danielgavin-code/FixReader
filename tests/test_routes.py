"""Smoke tests: public route availability, static assets, redirects, removed pages."""
import pytest

# ---------------------------------------------------------------------------
# Primary public routes — each must return 200
# ---------------------------------------------------------------------------

PUBLIC_200 = [
    '/',
    '/compare',
    '/tools/message-builder',
    '/tools/tag-validator',
    '/message-library',
    '/library',
    '/exchange-specs',
    '/resources',
    '/troubleshooting/network',
    '/troubleshooting/sequence-numbers',
    '/troubleshooting/logon',
    '/troubleshooting/fill-reconciliation',
    '/troubleshooting/rejects',
    '/troubleshooting/latency',
    '/troubleshooting/duplicate-orders',
    '/troubleshooting/gap-fill',
    '/tools/order-entry',
    '/tools/drop-copy',
    '/tools/allocation',
    '/cert/order-entry',
    '/cert/drop-copy',
    '/cert/allocation',
    '/reference/fix42',
    '/reference/fix44',
    '/reference/fix50',
    '/tag/35',
    '/tag/49',
    '/mic/XNYS',
    '/currency/USD',
    '/country/US',
    '/timezone/ET',
    '/timezone/UTC',
]


@pytest.mark.parametrize('path', PUBLIC_200)
def test_public_route_200(client, path):
    r = client.get(path)
    assert r.status_code == 200, f'{path} returned {r.status_code}'


# ---------------------------------------------------------------------------
# Static assets — must return 200
# ---------------------------------------------------------------------------

STATIC_200 = [
    '/static/css/main.css',
    '/static/js/search.js',
]


@pytest.mark.parametrize('path', STATIC_200)
def test_static_asset_200(client, path):
    r = client.get(path)
    assert r.status_code == 200, f'{path} returned {r.status_code}'


# ---------------------------------------------------------------------------
# Redirects — confirm status and destination
# ---------------------------------------------------------------------------

REDIRECTS = [
    # (path, expected_location)
    # /library is a canonical alias that renders directly (200), not a redirect
    ('/troubleshooting',       '/troubleshooting/network'),
    ('/tools',                 '/'),
    ('/about',                 '/'),
    ('/fix-specs',             '/message-library'),
    ('/field-reference',       '/message-library'),
    ('/reference',             '/message-library'),
    ('/tag-validator',         '/tools/tag-validator'),
    ('/validator',             '/tools/tag-validator'),
    ('/message-builder',       '/tools/message-builder'),
    ('/builder',               '/tools/message-builder'),
    ('/tools/cert-scripts',    '/cert/order-entry'),
    ('/mic',                   '/message-library'),
]


@pytest.mark.parametrize('path,destination', REDIRECTS)
def test_redirect_status(client, path, destination):
    r = client.get(path)
    assert r.status_code in (301, 302), f'{path} expected redirect, got {r.status_code}'


@pytest.mark.parametrize('path,destination', REDIRECTS)
def test_redirect_destination(client, path, destination):
    r = client.get(path)
    assert r.headers['Location'].rstrip('/') == destination.rstrip('/'), (
        f'{path} redirected to {r.headers["Location"]!r}, expected {destination!r}'
    )


@pytest.mark.parametrize('path,destination', REDIRECTS)
def test_redirect_lands_200(client, path, destination):
    r = client.get(path, follow_redirects=True)
    assert r.status_code == 200, f'Following {path} ended with {r.status_code}'


# ---------------------------------------------------------------------------
# Removed public pages — must return 404
# ---------------------------------------------------------------------------

REMOVED_404 = ['/contact', '/feedback']


@pytest.mark.parametrize('path', REMOVED_404)
def test_removed_pages_404(client, path):
    r = client.get(path)
    assert r.status_code == 404, f'{path} expected 404, got {r.status_code}'


# ---------------------------------------------------------------------------
# Invalid routes — must not return 500
# ---------------------------------------------------------------------------

def test_unknown_route_is_not_500(client):
    r = client.get('/this-does-not-exist')
    assert r.status_code != 500

def test_invalid_reference_version_404(client):
    r = client.get('/reference/badver')
    assert r.status_code == 404

def test_unknown_tag_404(client):
    r = client.get('/tag/99999')
    assert r.status_code == 404

def test_unknown_mic_404(client):
    r = client.get('/mic/ZZZZ')
    assert r.status_code == 404
