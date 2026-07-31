"""Wave 2 — search, navigation, breadcrumbs, and related content tests."""
import pytest


# ---------------------------------------------------------------------------
# Task 1 + 2: Search JS asset exists and contains expected features
# ---------------------------------------------------------------------------

def test_search_js_served(client):
    r = client.get('/static/js/search.js')
    assert r.status_code == 200
    js = r.data.decode('utf-8')
    # Core constants present
    assert 'FIELD_TO_TAG' in js
    assert '_CAT_KEY' in js
    assert '_CAT_LABELS' in js
    assert '_CAT_CAPS' in js
    assert '_CAT_ORDER' in js


def test_search_js_category_labels(client):
    r = client.get('/static/js/search.js')
    js = r.data.decode('utf-8')
    assert "'Tags'" in js
    assert "'Messages'" in js
    assert "'Enumeration Values'" in js
    assert "'Components'" in js
    assert "'Tools'" in js
    assert "'Exchange Specifications'" in js
    assert "'Troubleshooting'" in js


def test_search_js_field_to_tag_built_from_enum(client):
    r = client.get('/static/js/search.js')
    js = r.data.decode('utf-8')
    # FIELD_TO_TAG uses FIXREADER_TAG_ENUM as source
    assert 'FIXREADER_TAG_ENUM' in js
    idx_field = js.index('FIELD_TO_TAG')
    idx_enum  = js.index('FIXREADER_TAG_ENUM')
    # FIXREADER_TAG_ENUM defined before FIELD_TO_TAG
    assert idx_enum < idx_field


def test_search_js_msgtype_d_normalization(client):
    r = client.get('/static/js/search.js')
    js = r.data.decode('utf-8')
    # Field-name + value pattern handler present
    assert 'fieldValM' in js
    assert 'FIELD_TO_TAG[fieldValM[1].toLowerCase()]' in js


def test_search_js_improved_scorer_field_name(client):
    r = client.get('/static/js/search.js')
    js = r.data.decode('utf-8')
    # Field name exact match scoring present
    assert 'fieldL && fieldL === q' in js
    # Higher base score for tag match (90 vs old 80)
    assert 's += 90' in js


def test_search_js_result_limit_increased(client):
    r = client.get('/static/js/search.js')
    js = r.data.decode('utf-8')
    # Broad text query now returns up to 30 for category grouping
    assert '.slice(0, 30)' in js


def test_search_js_categorized_renderer(client):
    r = client.get('/static/js/search.js')
    js = r.data.decode('utf-8')
    # Category header rendered
    assert 'nav-search-cat-hdr' in js
    # Result items get id for aria-activedescendant
    assert "'nav-sr-'" in js
    assert "role=\"option\"" in js


# ---------------------------------------------------------------------------
# Task 3: Keyboard interaction and ARIA
# ---------------------------------------------------------------------------

def test_search_js_aria_initialization(client):
    r = client.get('/static/js/search.js')
    js = r.data.decode('utf-8')
    assert "setAttribute('role', 'combobox')" in js
    assert "setAttribute('aria-expanded'" in js
    assert "setAttribute('aria-autocomplete'" in js
    assert "setAttribute('aria-controls'" in js
    assert "setAttribute('aria-haspopup'" in js
    assert "setAttribute('role', 'listbox')" in js


def test_search_js_aria_expanded_set_on_show(client):
    r = client.get('/static/js/search.js')
    js = r.data.decode('utf-8')
    # aria-expanded true when results shown
    assert "setAttribute('aria-expanded', 'true')" in js
    # aria-expanded false when closed
    assert "setAttribute('aria-expanded', 'false')" in js


def test_search_js_aria_activedescendant(client):
    r = client.get('/static/js/search.js')
    js = r.data.decode('utf-8')
    assert 'aria-activedescendant' in js
    assert 'removeAttribute' in js


def test_search_js_slash_shortcut(client):
    r = client.get('/static/js/search.js')
    js = r.data.decode('utf-8')
    # / key opens search from page body
    assert "e.key !== '/'" in js
    assert '_prevFocus' in js
    assert 'isContentEditable' in js


def test_search_js_escape_restores_focus(client):
    r = client.get('/static/js/search.js')
    js = r.data.decode('utf-8')
    # Escape closes and restores prior focus
    assert "_prevFocus && _prevFocus !== input" in js
    assert "_prevFocus.focus()" in js


def test_search_js_click_outside_updates_aria(client):
    r = client.get('/static/js/search.js')
    js = r.data.decode('utf-8')
    # click-outside handler resets aria-expanded
    assert "removeAttribute('aria-activedescendant')" in js


# ---------------------------------------------------------------------------
# Task 4: Breadcrumbs — tag detail page
# ---------------------------------------------------------------------------

def test_tag_detail_has_breadcrumb(client):
    r = client.get('/tag/35')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    assert 'aria-label="Breadcrumb"' in html
    assert '<ol>' in html
    assert 'aria-current="page"' in html


def test_tag_detail_breadcrumb_links(client):
    r = client.get('/tag/35')
    html = r.data.decode('utf-8')
    assert 'href="/"' in html
    assert 'href="/message-library"' in html


def test_tag_detail_breadcrumb_current_page(client):
    r = client.get('/tag/35')
    html = r.data.decode('utf-8')
    assert 'Tag 35' in html
    assert 'MsgType' in html


def test_tag_detail_breadcrumb_tag_49(client):
    r = client.get('/tag/49')
    html = r.data.decode('utf-8')
    assert 'aria-label="Breadcrumb"' in html
    assert 'Tag 49' in html


# ---------------------------------------------------------------------------
# Task 4: Breadcrumbs — fix_reference page
# ---------------------------------------------------------------------------

def test_fix_reference_has_breadcrumb(client):
    r = client.get('/reference/fix42')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    assert 'aria-label="Breadcrumb"' in html
    assert 'aria-current="page"' in html


def test_fix_reference_breadcrumb_links(client):
    r = client.get('/reference/fix42')
    html = r.data.decode('utf-8')
    assert 'href="/"' in html
    assert 'href="/message-library"' in html


def test_fix_reference_breadcrumb_version(client):
    r = client.get('/reference/fix44')
    html = r.data.decode('utf-8')
    assert 'FIX 4.4' in html


# ---------------------------------------------------------------------------
# Task 4: Breadcrumbs — troubleshooting articles
# ---------------------------------------------------------------------------

TROUBLESHOOTING_BREADCRUMBS = [
    ('/troubleshooting/network',             'Network &amp; Connectivity'),
    ('/troubleshooting/sequence-numbers',    'Sequence Number Issues'),
    ('/troubleshooting/logon',               'Logon Failures'),
    ('/troubleshooting/fill-reconciliation', 'Fill Reconciliation'),
    ('/troubleshooting/rejects',             'Order Rejects'),
    ('/troubleshooting/latency',             'Latency &amp; Timing'),
    ('/troubleshooting/duplicate-orders',    'Duplicate Orders'),
    ('/troubleshooting/gap-fill',            'Gap Fill &amp; Resend'),
]


@pytest.mark.parametrize('path,label', TROUBLESHOOTING_BREADCRUMBS)
def test_troubleshooting_breadcrumb(client, path, label):
    r = client.get(path)
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    assert 'aria-label="Breadcrumb"' in html
    assert 'aria-current="page"' in html
    assert label in html


@pytest.mark.parametrize('path,_', TROUBLESHOOTING_BREADCRUMBS)
def test_troubleshooting_breadcrumb_home_link(client, path, _):
    r = client.get(path)
    html = r.data.decode('utf-8')
    assert 'href="/"' in html
    assert 'href="/troubleshooting"' in html


# ---------------------------------------------------------------------------
# Task 5: Related content on tag detail pages
# ---------------------------------------------------------------------------

def test_tag_35_related_section_exists(client):
    r = client.get('/tag/35')
    html = r.data.decode('utf-8')
    assert 'tr-related' in html
    assert 'Related' in html


def test_tag_35_fix_versions(client):
    r = client.get('/tag/35')
    html = r.data.decode('utf-8')
    # Tag 35 present across FIX versions — should show version chips
    assert 'tr-related-chip' in html
    assert '/reference/fix' in html


def test_tag_with_required_in_shows_messages(client):
    # Tag 6 (AvgPx) is required in Execution Report
    r = client.get('/tag/6')
    html = r.data.decode('utf-8')
    assert 'Required in' in html
    assert 'Execution Report' in html


def test_tag_with_optional_in_shows_messages(client):
    # Tag 1 (Account) is optional in New Order Single
    r = client.get('/tag/1')
    html = r.data.decode('utf-8')
    assert 'Optional in' in html
    assert 'New Order Single' in html


def test_tag_34_has_sequence_troubleshooting(client):
    r = client.get('/tag/34')
    html = r.data.decode('utf-8')
    assert 'Troubleshooting' in html
    assert '/troubleshooting/sequence-numbers' in html


def test_tag_43_has_duplicate_orders_troubleshooting(client):
    r = client.get('/tag/43')
    html = r.data.decode('utf-8')
    assert '/troubleshooting/duplicate-orders' in html


def test_tag_49_has_logon_troubleshooting(client):
    r = client.get('/tag/49')
    html = r.data.decode('utf-8')
    assert '/troubleshooting/logon' in html


def test_related_chips_link_to_correct_urls(client):
    r = client.get('/tag/35')
    html = r.data.decode('utf-8')
    # FIX version chips use correct URL format (no dots)
    assert '/reference/fix42' in html


# ---------------------------------------------------------------------------
# Task 4: Breadcrumb CSS present
# ---------------------------------------------------------------------------

def test_breadcrumb_css_served(client):
    r = client.get('/static/css/main.css')
    assert r.status_code == 200
    css = r.data.decode('utf-8')
    assert '.breadcrumb' in css
    assert 'aria-current' in css


def test_category_header_css_served(client):
    r = client.get('/static/css/main.css')
    css = r.data.decode('utf-8')
    assert '.nav-search-cat-hdr' in css


def test_related_content_css_served(client):
    r = client.get('/static/css/main.css')
    css = r.data.decode('utf-8')
    assert '.tr-related' in css
    assert '.tr-related-chip' in css
