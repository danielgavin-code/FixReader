"""Smoke tests: footer consistency across all rendered public pages."""
import pytest

MAILTO_TARGET = 'mailto:feedback@fixreader.org?subject=FIXReader.org%20Feedback'

# Every route that renders a full HTML page (excludes redirects, API endpoints,
# and detail pages that require a valid database key)
RENDERED_PAGES = [
    '/',
    '/compare',
    '/tools/message-builder',
    '/tools/tag-validator',
    '/message-library',
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
    '/reference/fix42',
    '/tag/35',
    '/mic/XNYS',
    '/currency/USD',
    '/country/US',
    '/timezone/ET',
]


def _html(client, path):
    r = client.get(path)
    assert r.status_code == 200, f'Expected 200 for {path}, got {r.status_code}'
    return r.data.decode('utf-8')


@pytest.mark.parametrize('path', RENDERED_PAGES)
def test_footer_has_feedback_mailto(client, path):
    html = _html(client, path)
    assert MAILTO_TARGET in html, (
        f'{path}: footer Feedback mailto link not found'
    )


@pytest.mark.parametrize('path', RENDERED_PAGES)
def test_footer_feedback_link_count(client, path):
    html = _html(client, path)
    count = html.count(MAILTO_TARGET)
    assert count == 1, (
        f'{path}: expected exactly 1 Feedback mailto link, found {count}'
    )


@pytest.mark.parametrize('path', RENDERED_PAGES)
def test_footer_no_contact_link(client, path):
    html = _html(client, path)
    assert 'href="/contact"' not in html, (
        f'{path}: found disallowed href="/contact" in page'
    )


@pytest.mark.parametrize('path', RENDERED_PAGES)
def test_footer_no_feedback_route_link(client, path):
    html = _html(client, path)
    assert 'href="/feedback"' not in html, (
        f'{path}: found disallowed href="/feedback" in page'
    )
