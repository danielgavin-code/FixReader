"""
Internal site crawl smoke test.

Starts at / and follows all internal HTML links, seeding route families
that are only reachable via JS-rendered navigation. Fails with a clear
diagnostic for every broken link found.
"""
import json
import os
import pytest
from tests.helpers.site_crawler import crawl

# ---------------------------------------------------------------------------
# Seed additional paths not reachable through static HTML links
# (JS-rendered from data files — verified to exist in the database)
# ---------------------------------------------------------------------------

def _tag_seeds():
    """Return /tag/<n> for every tag number in fix_tags.json."""
    data = os.path.join(os.path.dirname(__file__), '..', 'fixreader_data', 'fix_tags.json')
    with open(data) as f:
        return [f'/tag/{t["tag"]}' for t in json.load(f)]


def _mic_seeds():
    """Return a representative sample of /mic/<code> pages."""
    data = os.path.join(os.path.dirname(__file__), '..', 'fixreader_data', 'mic_codes.json')
    with open(data) as f:
        codes = [m['mic'] for m in json.load(f)]
    # Sample: first, middle, last — enough to exercise the template
    n = len(codes)
    sample = {codes[0], codes[n // 2], codes[-1], 'XNYS', 'XNAS', 'IEXG', 'XCBO'}
    return [f'/mic/{c}' for c in sample if c in codes]  # only codes in the DB


def _currency_seeds():
    data = os.path.join(os.path.dirname(__file__), '..', 'fixreader_data', 'currency_codes.json')
    with open(data) as f:
        codes = [c['code'] for c in json.load(f)]
    sample = {codes[0], codes[len(codes) // 2], codes[-1], 'USD', 'EUR', 'GBP'}
    return [f'/currency/{c}' for c in sample if c in codes]


def _country_seeds():
    data = os.path.join(os.path.dirname(__file__), '..', 'fixreader_data', 'country_codes.json')
    with open(data) as f:
        codes = [c['code'] for c in json.load(f)]
    sample = {codes[0], codes[len(codes) // 2], codes[-1], 'US', 'GB', 'JP'}
    return [f'/country/{c}' for c in sample if c in codes]


def _timezone_seeds():
    data = os.path.join(os.path.dirname(__file__), '..', 'fixreader_data', 'timezone_data.json')
    with open(data) as f:
        zones = [t['zone'].replace('/', '_').replace(' ', '_') for t in json.load(f)]
    return [f'/timezone/{z}' for z in zones]


def _extra_seeds():
    seeds = []
    seeds += _tag_seeds()
    seeds += _mic_seeds()
    seeds += _currency_seeds()
    seeds += _country_seeds()
    seeds += _timezone_seeds()
    return seeds


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.fixture(scope='module')
def crawl_result(client_module):
    """Run the crawl once per module; share results across tests."""
    return crawl(client_module, extra_seeds=_extra_seeds())


@pytest.fixture(scope='module')
def client_module():
    import app as _app
    _app.app.config['TESTING'] = True
    with _app.app.test_client() as c:
        yield c


def test_crawl_no_broken_links(crawl_result):
    """Every reachable internal URL must respond without error."""
    assert crawl_result.ok(), (
        f'Internal crawl found {len(crawl_result.failures)} broken link(s):\n\n'
        + crawl_result.failure_report()
    )


def test_crawl_coverage(crawl_result):
    """Crawl must visit a meaningful number of URLs (catches misconfigured seeding)."""
    count = len(crawl_result.visited)
    assert count >= 50, (
        f'Crawl only visited {count} URLs — seeding may be broken'
    )


def test_crawl_no_contact_links(client_module):
    """No rendered public page may link to /contact."""
    pages_to_check = [
        '/', '/compare', '/message-library', '/exchange-specs', '/resources',
        '/tools/message-builder', '/tools/tag-validator',
        '/troubleshooting/network', '/cert/order-entry',
    ]
    violations = []
    for path in pages_to_check:
        r = client_module.get(path)
        if r.status_code == 200 and b'href="/contact"' in r.data:
            violations.append(path)
    assert not violations, (
        f'Pages still link to removed /contact route: {violations}'
    )


def test_crawl_no_feedback_route_links(client_module):
    """No rendered public page may link to /feedback (the route; mailto is fine)."""
    pages_to_check = [
        '/', '/compare', '/message-library', '/exchange-specs', '/resources',
        '/tools/message-builder', '/tools/tag-validator',
        '/troubleshooting/network', '/cert/order-entry',
    ]
    violations = []
    for path in pages_to_check:
        r = client_module.get(path)
        if r.status_code == 200 and b'href="/feedback"' in r.data:
            violations.append(path)
    assert not violations, (
        f'Pages still link to removed /feedback route: {violations}'
    )


def test_crawl_visited_count_reported(crawl_result, capsys):
    """Non-assertion: print crawl summary to stdout for visibility."""
    print(f'\nCrawl summary: {len(crawl_result.visited)} URLs visited, '
          f'{len(crawl_result.failures)} failures')
