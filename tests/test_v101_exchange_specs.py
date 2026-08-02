"""v1.0.1 QA tests: Exchange Specs navigation audit.

Every exchange visible in the UI must:
  - have a version-bar pill with the correct key and MIC label
  - have a sidebar item with the correct key, data-key, and MIC label
  - be backed by an entry in the EXCHANGES JS data block
  - match pill label == data MIC (no stale or duplicate labels)

Root bug fixed: clicking NYSE Arca (or any exchange) could open a different
exchange when navigating via a URL hash (#arca, etc.) because the init always
showed NYSE and ignored window.location.hash.

Additional bugs fixed:
  - bzx pill/sidebar showed XCBO (should be BATS)
  - byx pill hardcoded class="active" before JS ran
  - nasdaq sidebar hardcoded class="active" before JS ran
  - no history.replaceState → hash URL never updated; deep-links always opened NYSE
"""
import re
import pytest


@pytest.fixture()
def exchange_html(client):
    r = client.get('/exchange-specs')
    assert r.status_code == 200
    return r.data.decode('utf-8')


# ── Gold-standard mapping: key → expected pill/sidebar MIC label ─────────────
EXPECTED = {
    'nyse':         'XNYS',
    'nasdaq':       'XNAS',
    'arca':         'ARCX',
    'bzx':          'BATS',
    'edgx':         'EDGX',
    'edga':         'EDGA',
    'iex':          'IEXG',
    'byx':          'BATY',
    'american':     'XASE',
    'national':     'XCIS',
    'nasdaqbx':     'XBOS',
    'memx':         'MEMX',
    'cboeopt':      'XCBO',
    'cboec2':       'C2OX',
    'bato':         'BATO',
    'edgo':         'EDGO',
    'phlx':         'XPHL',
    'ise':          'XISX',
    'gemx':         'GMNI',
    'mrx':          'MCRY',
    'bxopt':        'XBXO',
    'amexopt':      'XASE',
    'arcaopt':      'ARCO',
    'miax':         'MIAX',
    'miaxpearl':    'MPRL',
    'miaxemerald':  'EMLD',
    'box':          'XBOX',
    'memxopt':      'MXOP',
    'iexopt':       'IEXO',
}


def _pill_map(html):
    """Extract {key: label} from version-bar pills (onclick="selectExchange('key',this)")."""
    pairs = re.findall(r"onclick=\"selectExchange\('([^']+)',this\)\"[^>]*>([^<]+)<", html)
    return {k: v.strip() for k, v in pairs}


def _sidebar_map(html):
    """Extract {key: label} from sidebar data-key attributes and adjacent ml-msg-code spans."""
    items = re.findall(
        r'data-key="([^"]+)"[^>]*>.*?<span class="ml-msg-code">([^<]+)</span>',
        html, re.DOTALL
    )
    return {k: v.strip() for k, v in items}


def _data_mics(html):
    """Extract {key: mic} from the EXCHANGES JS const in the page source."""
    exchanges_block = re.search(r'const EXCHANGES = \{(.+?)\n\};', html, re.DOTALL)
    if not exchanges_block:
        return {}
    body = exchanges_block.group(1)
    keys = re.findall(r'^  (\w+): \{', body, re.MULTILINE)
    mics = re.findall(r"mic: '([^']+)'", body)
    return dict(zip(keys, mics))


# ── Page smoke ────────────────────────────────────────────────────────────────

def test_exchange_specs_returns_200(client):
    r = client.get('/exchange-specs')
    assert r.status_code == 200


# ── All 29 exchanges present ──────────────────────────────────────────────────

def test_all_29_exchanges_have_pills(exchange_html):
    pills = _pill_map(exchange_html)
    missing = [k for k in EXPECTED if k not in pills]
    assert not missing, f'Pills missing for exchanges: {missing}'


def test_all_29_exchanges_have_sidebar_items(exchange_html):
    sidebar = _sidebar_map(exchange_html)
    missing = [k for k in EXPECTED if k not in sidebar]
    assert not missing, f'Sidebar missing for exchanges: {missing}'


def test_all_29_exchanges_in_data(exchange_html):
    data = _data_mics(exchange_html)
    missing = [k for k in EXPECTED if k not in data]
    assert not missing, f'EXCHANGES data missing keys: {missing}'


# ── Per-exchange: pill label matches expected MIC ─────────────────────────────

@pytest.mark.parametrize('key,mic', list(EXPECTED.items()))
def test_pill_label_matches_mic(key, mic, exchange_html):
    pills = _pill_map(exchange_html)
    assert key in pills, f'No pill for {key}'
    assert pills[key] == mic, (
        f'Pill for {key}: expected {mic!r}, got {pills[key]!r}'
    )


# ── Per-exchange: sidebar label matches expected MIC ─────────────────────────

@pytest.mark.parametrize('key,mic', list(EXPECTED.items()))
def test_sidebar_label_matches_mic(key, mic, exchange_html):
    sidebar = _sidebar_map(exchange_html)
    assert key in sidebar, f'No sidebar item for {key}'
    assert sidebar[key] == mic, (
        f'Sidebar for {key}: expected {mic!r}, got {sidebar[key]!r}'
    )


# ── Per-exchange: data MIC matches expected MIC ───────────────────────────────

@pytest.mark.parametrize('key,mic', list(EXPECTED.items()))
def test_data_mic_matches_expected(key, mic, exchange_html):
    data = _data_mics(exchange_html)
    assert key in data, f'No EXCHANGES data entry for {key}'
    assert data[key] == mic, (
        f'EXCHANGES[{key}].mic: expected {mic!r}, got {data[key]!r}'
    )


# ── Specific regression: bzx must not show XCBO ──────────────────────────────

def test_bzx_pill_is_bats_not_xcbo(exchange_html):
    pills = _pill_map(exchange_html)
    assert pills.get('bzx') == 'BATS', (
        f"bzx pill should be 'BATS' (was 'XCBO' before v1.0.1 fix), got {pills.get('bzx')!r}"
    )


def test_bzx_sidebar_is_bats_not_xcbo(exchange_html):
    sidebar = _sidebar_map(exchange_html)
    assert sidebar.get('bzx') == 'BATS', (
        f"bzx sidebar should be 'BATS' (was 'XCBO' before v1.0.1 fix), got {sidebar.get('bzx')!r}"
    )


def test_xcbo_label_appears_exactly_once_in_pills(exchange_html):
    """Only cboeopt should show XCBO; bzx was the duplicate that was fixed."""
    pills = _pill_map(exchange_html)
    xcbo_keys = [k for k, v in pills.items() if v == 'XCBO']
    assert xcbo_keys == ['cboeopt'], (
        f'Expected only cboeopt to have XCBO pill, got: {xcbo_keys}'
    )


# ── No hardcoded stale active states ─────────────────────────────────────────

def test_no_hardcoded_active_pill(exchange_html):
    """No pill should have class="ex-pill active" hardcoded in HTML; JS owns active state."""
    assert 'ex-pill active' not in exchange_html, (
        'Found hardcoded ex-pill active — JS should manage active state, not static HTML'
    )


def test_no_hardcoded_active_sidebar_item(exchange_html):
    """No sidebar item should have class="ml-msg-item active" hardcoded in HTML."""
    assert 'ml-msg-item active' not in exchange_html, (
        'Found hardcoded ml-msg-item active — JS should manage active state, not static HTML'
    )


# ── Hash routing and deep-link fix ───────────────────────────────────────────

def test_push_state_used_for_user_selection(exchange_html):
    """selectExchange must call history.pushState so Back/Forward work between exchanges."""
    assert 'history.pushState' in exchange_html, (
        'history.pushState not found — Back/Forward between exchanges will not work'
    )


def test_replace_state_used_for_init(exchange_html):
    """Init must use history.replaceState (not pushState) so back does not revisit a stale default."""
    assert 'history.replaceState' in exchange_html, (
        'history.replaceState not found — init should replace (not push) the initial history entry'
    )


def test_popstate_listener_present(exchange_html):
    """A popstate event listener is required for Back/Forward navigation between exchanges."""
    assert 'popstate' in exchange_html, (
        'popstate listener not found — Back/Forward between exchanges will not update content'
    )


def test_hash_aware_init_present(exchange_html):
    """Init must read window.location.hash so /exchange-specs#arca shows Arca."""
    assert "EXCHANGES[_h]" in exchange_html, (
        'Hash-aware init not found — navigating to /exchange-specs#arca would show NYSE instead'
    )


def test_init_reads_window_location_hash(exchange_html):
    assert 'window.location.hash' in exchange_html, (
        'window.location.hash not found in init — hash-based routing will not work'
    )


# ── Sidebar keys match pill keys (completeness cross-check) ──────────────────

def test_sidebar_and_pill_keys_match(exchange_html):
    pills = set(_pill_map(exchange_html).keys())
    sidebar = set(_sidebar_map(exchange_html).keys())
    assert pills == sidebar, (
        f'Pills and sidebar have different exchange sets. '
        f'Pills only: {pills - sidebar}. Sidebar only: {sidebar - pills}.'
    )


# ── Sidebar data-key attributes match onclick keys ────────────────────────────

def test_sidebar_data_key_matches_onclick(exchange_html):
    """Each sidebar <a> element: data-key must match the key in onclick selectExchange."""
    items = re.findall(
        r'data-key="([^"]+)"[^>]*onclick="selectExchange\(\'([^\']+)\'',
        exchange_html
    )
    mismatches = [(dk, oc) for dk, oc in items if dk != oc]
    assert not mismatches, f'data-key / onclick mismatches: {mismatches}'


# ── Pill aria-selected sanity ─────────────────────────────────────────────────

def test_no_pill_hardcoded_aria_selected_true(exchange_html):
    """No pill should have aria-selected=true hardcoded before JS runs."""
    count = exchange_html.count('aria-selected="true"')
    assert count == 0, (
        f'Found {count} hardcoded aria-selected="true" in pills — '
        f'all pills should start with aria-selected="false"; JS toggles the active one'
    )
