"""
Automated accessibility checks for primary public pages.

Covers: h1 count, viewport meta, duplicate IDs, form labels,
nav aria-label, and examples-button element type.
"""
import re
import pytest

PRIMARY_PAGES = [
    '/',
    '/compare',
    '/tools/tag-validator',
    '/tools/message-builder',
    '/message-library',
    '/exchange-specs',
    '/resources',
    '/troubleshooting/network',
    '/troubleshooting/sequence-numbers',
    '/troubleshooting/logon',
    '/reference/fix42',
    '/tag/35',
]

_RE_H1            = re.compile(r'<h1[\s>]', re.IGNORECASE)
_RE_VIEWPORT      = re.compile(r'<meta[^>]+name=["\']viewport["\']', re.IGNORECASE)
_RE_ID            = re.compile(r'\bid=["\']([^"\']+)["\']', re.IGNORECASE)
_RE_TYPE_HIDDEN   = re.compile(r'\btype=["\']hidden["\']', re.IGNORECASE)
_RE_TYPE_SUBMIT   = re.compile(r'\btype=["\'](?:submit|button|reset)["\']', re.IGNORECASE)
_RE_TYPE_CHKRADIO = re.compile(r'\btype=["\'](?:checkbox|radio)["\']', re.IGNORECASE)
_RE_ARIA_LABEL    = re.compile(r'\baria-label(?:ledby)?=["\'][^"\']+["\']', re.IGNORECASE)
_RE_ID_ATTR       = re.compile(r'\bid=["\']([^"\']+)["\']', re.IGNORECASE)
_RE_LABEL_FOR     = re.compile(r'<label\b[^>]*\bfor=["\']([^"\']+)["\']', re.IGNORECASE)
_RE_SCRIPT        = re.compile(r'<script\b[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE)


def _html(client, path):
    r = client.get(path)
    assert r.status_code == 200, f'{path} returned {r.status_code}'
    return r.data.decode('utf-8', errors='ignore')


def _strip_scripts(html):
    """Remove <script>...</script> blocks so we only inspect real DOM markup."""
    return _RE_SCRIPT.sub('', html)


def _is_inside_label(html, match_start):
    """True if the element at match_start is a descendant of an open <label> tag."""
    before = html[:match_start]
    open_labels  = len(re.findall(r'<label\b', before, re.IGNORECASE))
    close_labels = len(re.findall(r'</label>', before, re.IGNORECASE))
    return open_labels > close_labels


# ── One <h1> per page ────────────────────────────────────────────

@pytest.mark.parametrize('path', PRIMARY_PAGES)
def test_exactly_one_h1(client, path):
    html = _html(client, path)
    count = len(_RE_H1.findall(html))
    assert count >= 1, f'{path} has no <h1>'
    assert count == 1, f'{path} has {count} <h1> elements (expected exactly 1)'


# ── Viewport meta tag present ─────────────────────────────────────

@pytest.mark.parametrize('path', PRIMARY_PAGES)
def test_viewport_meta_present(client, path):
    html = _html(client, path)
    assert _RE_VIEWPORT.search(html), f'{path} is missing <meta name="viewport">'


# ── No duplicate IDs in server-rendered HTML ──────────────────────

@pytest.mark.parametrize('path', PRIMARY_PAGES)
def test_no_duplicate_ids(client, path):
    html = _strip_scripts(_html(client, path))
    ids = _RE_ID.findall(html)
    seen = {}
    for id_val in ids:
        seen[id_val] = seen.get(id_val, 0) + 1
    dupes = [k for k, v in seen.items() if v > 1]
    assert not dupes, f'{path} has duplicate IDs: {dupes}'


# ── Visible <input> and <textarea> controls have labels ───────────

@pytest.mark.parametrize('path', PRIMARY_PAGES)
def test_form_controls_have_labels(client, path):
    html = _strip_scripts(_html(client, path))

    # IDs covered by an explicit <label for="...">
    labelled_ids = set(m.group(1) for m in _RE_LABEL_FOR.finditer(html))

    unlabelled = []

    for m in re.finditer(r'<input\b([^>]*)>', html, re.IGNORECASE):
        attrs = m.group(1)
        # Skip non-interactive types
        if _RE_TYPE_HIDDEN.search(attrs) or _RE_TYPE_SUBMIT.search(attrs):
            continue
        # Checkbox/radio with implicit label (wrapped in <label>…</label>)
        if _RE_TYPE_CHKRADIO.search(attrs) and _is_inside_label(html, m.start()):
            continue
        if _RE_ARIA_LABEL.search(attrs):
            continue
        id_m = _RE_ID_ATTR.search(attrs)
        if id_m and id_m.group(1) in labelled_ids:
            continue
        unlabelled.append(m.group(0)[:120])

    for m in re.finditer(r'<textarea\b([^>]*)>', html, re.IGNORECASE):
        attrs = m.group(1)
        if _RE_ARIA_LABEL.search(attrs):
            continue
        id_m = _RE_ID_ATTR.search(attrs)
        if id_m and id_m.group(1) in labelled_ids:
            continue
        unlabelled.append(m.group(0)[:120])

    assert not unlabelled, (
        f'{path} has {len(unlabelled)} form control(s) without accessible labels:\n'
        + '\n'.join(unlabelled)
    )


# ── <nav> elements have aria-label ───────────────────────────────

@pytest.mark.parametrize('path', PRIMARY_PAGES)
def test_nav_has_aria_label(client, path):
    html = _html(client, path)
    navs = re.findall(r'<nav\b[^>]*>', html, re.IGNORECASE)
    unlabelled = [n for n in navs if not re.search(r'\baria-label=["\']', n, re.IGNORECASE)]
    assert not unlabelled, (
        f'{path} has <nav> elements without aria-label: {unlabelled}'
    )


# ── Examples toggle button is a real <button> ─────────────────────

def test_decoder_examples_button_is_button(client):
    html = _strip_scripts(_html(client, '/'))
    assert 'class="examples-drop-item"' in html, 'examples-drop-item class not found'
    items = re.findall(r'<(\w+)\s[^>]*class="examples-drop-item"', html)
    non_buttons = [t for t in items if t.lower() != 'button']
    assert not non_buttons, (
        f'Decoder examples dropdown has non-button interactive items: {non_buttons}'
    )


# ── aria-expanded present on examples toggle buttons ─────────────

@pytest.mark.parametrize('path,btn_id', [
    ('/', 'examples-btn'),
    ('/tools/tag-validator', 'val-examples-btn'),
])
def test_examples_btn_has_aria_expanded(client, path, btn_id):
    html = _html(client, path)
    pattern = re.compile(
        r'<button\b[^>]*\bid=["\']' + re.escape(btn_id) + r'["\'][^>]*>',
        re.IGNORECASE,
    )
    m = pattern.search(html)
    assert m, f'{path}: button #{btn_id} not found'
    assert 'aria-expanded=' in m.group(0), (
        f'{path}: button #{btn_id} missing aria-expanded'
    )
