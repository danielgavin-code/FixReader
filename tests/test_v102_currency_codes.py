"""v1.0.2 QA tests: Currency Codes — correct principal-country assignments.

Root bug: first-row-wins deduplication during initial ISO 4217 import chose
alphabetically-earlier territories (e.g. American Samoa) over the principal
issuing country/region (United States) for multi-country currencies.

Fixes applied:
- currency_codes.json: 23 corrected country fields
- templates/message_library.html CCY_DATA inline JS: same 23 corrections
- CCY_TO_COUNTRY flag maps: removed arbitrary member-country flags for
  shared-zone currencies (XAF, XOF, XPF, XCD) and special codes

Both data sources must stay in sync; tests verify both independently.
"""
import json
import os
import re
import random
import pytest


# ── Canonical corrections ─────────────────────────────────────────────────────

CORRECTIONS = {
    # Incorrect principal-country selections
    'CHF': 'Switzerland',
    'EUR': 'Euro area',
    'GBP': 'United Kingdom',
    'INR': 'India',
    'NOK': 'Norway',
    'NZD': 'New Zealand',
    'USD': 'United States',
    'ZAR': 'South Africa',
    # Shared currencies incorrectly assigned to one member
    'XAF': 'Central African Economic and Monetary Community (CEMAC)',
    'XCD': 'Eastern Caribbean Currency Union (ECCU)',
    'XCG': 'Curaçao and Sint Maarten',
    'XOF': 'West African Economic and Monetary Union (WAEMU/UEMOA)',
    'XPF': 'French Pacific territories',
    # Special ISO codes — no ZZ... placeholder values
    'XAG': 'Precious metal — Silver',
    'XAU': 'Precious metal — Gold',
    'XBA': 'Supranational unit — EURCO',
    'XBB': 'Supranational unit — EMU-6',
    'XBC': 'Supranational unit — EUA-9',
    'XBD': 'Supranational unit — EUA-17',
    'XPD': 'Precious metal — Palladium',
    'XPT': 'Precious metal — Platinum',
    'XTS': 'Testing code',
    'XXX': 'No currency involved',
}

# Previous wrong values that must not appear anywhere in the corrected pages
WRONG_VALUES = {
    'CHF': 'LIECHTENSTEIN',
    'EUR': 'ÅLAND ISLANDS',
    'GBP': 'GUERNSEY',
    'INR': 'BHUTAN',
    'NOK': 'BOUVET ISLAND',
    'NZD': 'COOK ISLANDS',
    'USD': 'AMERICAN SAMOA',
    'ZAR': 'LESOTHO',
    'XAF': 'CAMEROON',
    'XCD': 'ANGUILLA',
    'XCG': 'CURAÇAO',
    'XOF': 'BENIN',
    'XPF': 'FRENCH POLYNESIA',
    'XAG': 'ZZ11_Silver',
    'XAU': 'ZZ08_Gold',
    'XBA': 'ZZ01_Bond',
    'XBB': 'ZZ02_Bond',
    'XBC': 'ZZ03_Bond',
    'XBD': 'ZZ04_Bond',
    'XPD': 'ZZ09_Palladium',
    'XPT': 'ZZ10_Platinum',
    'XTS': 'ZZ06_Testing_Code',
    'XXX': 'ZZ07_No_Currency',
}

_BASE = os.path.dirname(os.path.dirname(__file__))
_JSON_PATH = os.path.join(_BASE, 'fixreader_data', 'currency_codes.json')


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_json():
    with open(_JSON_PATH, encoding='utf-8') as f:
        return {r['code']: r for r in json.load(f)}


def _ccy_data_from_html(html):
    """Extract {code: country} from CCY_DATA inline JS in message_library.html."""
    block = re.search(r'const CCY_DATA = \[(.+?)\];', html, re.DOTALL)
    if not block:
        return {}
    pairs = re.findall(r'code:"([^"]+)"[^}]*?country:"([^"]+)"', block.group(1), re.DOTALL)
    return {code: country for code, country in pairs}


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture()
def library_html(client):
    r = client.get('/message-library')
    assert r.status_code == 200
    return r.data.decode('utf-8')


# ── JSON data tests ───────────────────────────────────────────────────────────

def test_json_loads_successfully():
    data = _load_json()
    assert len(data) >= 177


@pytest.mark.parametrize('code,expected_country', list(CORRECTIONS.items()))
def test_json_correct_country(code, expected_country):
    data = _load_json()
    assert code in data, f'Code {code} not found in currency_codes.json'
    assert data[code]['country'] == expected_country, (
        f'{code}: expected {expected_country!r}, got {data[code]["country"]!r}'
    )


@pytest.mark.parametrize('code,wrong_country', list(WRONG_VALUES.items()))
def test_json_no_wrong_country(code, wrong_country):
    data = _load_json()
    if code not in data:
        return
    country = data[code]['country']
    # Case-sensitive: old values were ALL CAPS; new correct values are mixed case
    assert wrong_country not in country, (
        f'{code}: old wrong value {wrong_country!r} still present in JSON: {country!r}'
    )


def test_json_no_zz_placeholders():
    data = _load_json()
    for code, record in data.items():
        country = record.get('country', '')
        assert not country.startswith('ZZ'), (
            f'{code}: raw ZZ placeholder still in JSON: {country!r}'
        )


# ── Canonical single-source requirement ──────────────────────────────────────

def test_json_no_duplicate_codes():
    with open(_JSON_PATH, encoding='utf-8') as f:
        records = json.load(f)
    codes = [r['code'] for r in records]
    seen = set()
    dupes = []
    for c in codes:
        if c in seen:
            dupes.append(c)
        seen.add(c)
    assert not dupes, f'Duplicate currency codes in JSON: {dupes}'


# ── Detail page tests ─────────────────────────────────────────────────────────

@pytest.mark.parametrize('code', list(CORRECTIONS.keys()))
def test_detail_page_returns_200(client, code):
    r = client.get(f'/currency/{code}')
    assert r.status_code == 200, f'/currency/{code} returned {r.status_code}'


@pytest.mark.parametrize('code,expected_country', list(CORRECTIONS.items()))
def test_detail_page_correct_country(client, code, expected_country):
    r = client.get(f'/currency/{code}')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    assert expected_country in html, (
        f'/currency/{code}: expected to find {expected_country!r} in page'
    )


@pytest.mark.parametrize('code,wrong_country', list(WRONG_VALUES.items()))
def test_detail_page_no_wrong_country(client, code, wrong_country):
    r = client.get(f'/currency/{code}')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    assert wrong_country not in html, (
        f'/currency/{code}: old wrong value {wrong_country!r} still appears in page'
    )


# Explicit positive assertions per spec ──────────────────────────────────────

def test_usd_shows_united_states(client):
    html = client.get('/currency/USD').data.decode('utf-8')
    assert 'United States' in html

def test_usd_not_american_samoa(client):
    html = client.get('/currency/USD').data.decode('utf-8')
    assert 'AMERICAN SAMOA' not in html
    assert 'American Samoa' not in html

def test_eur_shows_euro_area(client):
    html = client.get('/currency/EUR').data.decode('utf-8')
    assert 'Euro area' in html

def test_eur_not_aland_islands(client):
    html = client.get('/currency/EUR').data.decode('utf-8')
    assert 'ÅLAND ISLANDS' not in html
    assert 'Åland Islands' not in html

def test_gbp_shows_united_kingdom(client):
    html = client.get('/currency/GBP').data.decode('utf-8')
    assert 'United Kingdom' in html

def test_gbp_not_guernsey(client):
    html = client.get('/currency/GBP').data.decode('utf-8')
    assert 'GUERNSEY' not in html
    assert 'Guernsey' not in html

def test_chf_shows_switzerland(client):
    html = client.get('/currency/CHF').data.decode('utf-8')
    assert 'Switzerland' in html

def test_chf_not_liechtenstein(client):
    html = client.get('/currency/CHF').data.decode('utf-8')
    assert 'LIECHTENSTEIN' not in html
    assert 'Liechtenstein' not in html

def test_inr_shows_india(client):
    html = client.get('/currency/INR').data.decode('utf-8')
    assert 'India' in html

def test_inr_not_bhutan(client):
    html = client.get('/currency/INR').data.decode('utf-8')
    assert 'BHUTAN' not in html
    assert 'Bhutan' not in html

def test_nok_shows_norway(client):
    html = client.get('/currency/NOK').data.decode('utf-8')
    assert 'Norway' in html

def test_nok_not_bouvet_island(client):
    html = client.get('/currency/NOK').data.decode('utf-8')
    assert 'BOUVET ISLAND' not in html
    assert 'Bouvet Island' not in html

def test_nzd_shows_new_zealand(client):
    html = client.get('/currency/NZD').data.decode('utf-8')
    assert 'New Zealand' in html

def test_nzd_not_cook_islands(client):
    html = client.get('/currency/NZD').data.decode('utf-8')
    assert 'COOK ISLANDS' not in html
    assert 'Cook Islands' not in html

def test_zar_shows_south_africa(client):
    html = client.get('/currency/ZAR').data.decode('utf-8')
    assert 'South Africa' in html

def test_zar_not_lesotho(client):
    html = client.get('/currency/ZAR').data.decode('utf-8')
    assert 'LESOTHO' not in html
    assert 'Lesotho' not in html

def test_xag_shows_precious_metal(client):
    html = client.get('/currency/XAG').data.decode('utf-8')
    assert 'Precious metal' in html
    assert 'ZZ11_Silver' not in html

def test_xau_shows_precious_metal(client):
    html = client.get('/currency/XAU').data.decode('utf-8')
    assert 'Precious metal' in html
    assert 'ZZ08_Gold' not in html

def test_xts_shows_testing_code(client):
    html = client.get('/currency/XTS').data.decode('utf-8')
    assert 'Testing code' in html
    assert 'ZZ06_Testing_Code' not in html

def test_xxx_shows_no_currency(client):
    html = client.get('/currency/XXX').data.decode('utf-8')
    assert 'No currency involved' in html
    assert 'ZZ07_No_Currency' not in html


# ── No ZZ placeholders on detail pages ───────────────────────────────────────

@pytest.mark.parametrize('code', ['XAG','XAU','XBA','XBB','XBC','XBD','XPD','XPT','XTS','XXX'])
def test_detail_no_zz_placeholder(client, code):
    html = client.get(f'/currency/{code}').data.decode('utf-8')
    assert 'ZZ0' not in html and 'ZZ1' not in html, (
        f'/currency/{code}: raw ZZ placeholder still visible in page'
    )


# ── CCY_DATA (message_library) tests ─────────────────────────────────────────

@pytest.mark.parametrize('code,expected_country', list(CORRECTIONS.items()))
def test_library_ccy_data_correct_country(library_html, code, expected_country):
    data = _ccy_data_from_html(library_html)
    assert code in data, f'Code {code} not found in CCY_DATA on message_library page'
    assert data[code] == expected_country, (
        f'CCY_DATA[{code}]: expected {expected_country!r}, got {data[code]!r}'
    )


@pytest.mark.parametrize('code,wrong_country', list(WRONG_VALUES.items()))
def test_library_no_wrong_country_in_ccy_data(library_html, code, wrong_country):
    data = _ccy_data_from_html(library_html)
    if code not in data:
        return
    # Case-sensitive: old values were ALL CAPS; new correct values are mixed case
    assert wrong_country not in data[code], (
        f'CCY_DATA[{code}]: old wrong value {wrong_country!r} still present: {data[code]!r}'
    )


def test_library_no_zz_placeholders_in_ccy_data(library_html):
    data = _ccy_data_from_html(library_html)
    bad = {code: country for code, country in data.items() if country.startswith('ZZ')}
    assert not bad, f'ZZ placeholders still in CCY_DATA: {bad}'


# ── JSON / CCY_DATA consistency ───────────────────────────────────────────────

def test_json_and_ccy_data_agree(library_html):
    """Both data sources must show identical country values for all 23 corrected codes."""
    json_data = _load_json()
    ccy_data = _ccy_data_from_html(library_html)
    mismatches = []
    for code in CORRECTIONS:
        json_val = json_data.get(code, {}).get('country', 'MISSING_IN_JSON')
        ccy_val = ccy_data.get(code, 'MISSING_IN_CCY_DATA')
        if json_val != ccy_val:
            mismatches.append((code, json_val, ccy_val))
    assert not mismatches, (
        'JSON and CCY_DATA disagree on:\n' +
        '\n'.join(f'  {c}: JSON={j!r} CCY_DATA={d!r}' for c, j, d in mismatches)
    )


# ── Entire-dataset link test ──────────────────────────────────────────────────

def test_all_currency_detail_pages_return_200(client):
    data = _load_json()
    failed = []
    for code in data:
        r = client.get(f'/currency/{code}')
        if r.status_code != 200:
            failed.append((code, r.status_code))
    assert not failed, f'Currency detail pages returned non-200: {failed}'


def test_all_detail_pages_show_correct_code(client):
    data = _load_json()
    failed = []
    for code in data:
        r = client.get(f'/currency/{code}')
        if r.status_code != 200:
            continue
        html = r.data.decode('utf-8')
        if code not in html:
            failed.append(code)
    assert not failed, f'Detail pages missing their own currency code in content: {failed}'


def test_all_detail_pages_country_matches_json(client):
    data = _load_json()
    mismatches = []
    for code, record in data.items():
        r = client.get(f'/currency/{code}')
        if r.status_code != 200:
            continue
        html = r.data.decode('utf-8')
        expected = record['country']
        if expected not in html:
            mismatches.append((code, expected))
    assert not mismatches, (
        'Detail pages missing expected country value from JSON:\n' +
        '\n'.join(f'  {c}: {v!r}' for c, v in mismatches)
    )


def test_no_duplicate_currency_routes(client):
    data = _load_json()
    codes_seen = set()
    for code in data:
        assert code not in codes_seen, f'Duplicate currency route for {code}'
        codes_seen.add(code)


# ── Determinism test ─────────────────────────────────────────────────────────

def test_corrections_stable_regardless_of_input_order():
    """The JSON file must contain the canonical value regardless of record order."""
    with open(_JSON_PATH, encoding='utf-8') as f:
        records = json.load(f)

    shuffled = records.copy()
    random.seed(42)
    random.shuffle(shuffled)

    # Build lookup from both orderings
    orig_lookup = {r['code']: r['country'] for r in records}
    shuf_lookup = {r['code']: r['country'] for r in shuffled}

    for code, expected in CORRECTIONS.items():
        assert orig_lookup.get(code) == expected, (
            f'{code}: original order gives wrong value {orig_lookup.get(code)!r}'
        )
        assert shuf_lookup.get(code) == expected, (
            f'{code}: shuffled order gives wrong value {shuf_lookup.get(code)!r}'
        )


# ── Flag / icon tests ─────────────────────────────────────────────────────────

def test_detail_usd_has_us_flag_code(client):
    """USD detail page CCY_TO_COUNTRY must map to 'US'."""
    html = client.get('/currency/USD').data.decode('utf-8')
    assert "'USD':'US'" in html or '"USD":"US"' in html, (
        'USD detail page CCY_TO_COUNTRY should map USD to US'
    )


def test_detail_shared_currencies_no_member_flag(client):
    """Shared-zone currencies must not show an arbitrary member-country flag."""
    flag_codes_to_ban = {
        'XAF': ['CM', 'CF', 'TD', 'GQ', 'GA', 'CG'],  # CEMAC members
        'XOF': ['SN', 'BJ', 'BF', 'CI', 'GW', 'ML', 'NE', 'TG'],  # WAEMU members
        'XPF': ['PF', 'NC', 'WF'],  # French Pacific territories
        'XCD': ['AG', 'AI', 'DM', 'GD', 'KN', 'LC', 'MS', 'VC'],  # ECCU members
    }
    for code, banned_flags in flag_codes_to_ban.items():
        html = client.get(f'/currency/{code}').data.decode('utf-8')
        for flag in banned_flags:
            # Check CCY_TO_COUNTRY assignment only (not general page content)
            pattern = f"'{code}':'{flag}'"
            assert pattern not in html, (
                f'/currency/{code}: CCY_TO_COUNTRY still maps to member-country flag {flag!r}'
            )


# ── BTN / LSL — own-currency non-contamination ───────────────────────────────
# BTN (Bhutan's Ngultrum) and LSL (Lesotho's Loti) were at risk of receiving
# incorrect country values during the 23-record fix because INR and ZAR
# previously had "BHUTAN" and "LESOTHO" as country values too.  These tests
# confirm the fix did not contaminate unrelated records.

def test_btn_detail_returns_200(client):
    assert client.get('/currency/BTN').status_code == 200

def test_btn_detail_shows_bhutan(client):
    html = client.get('/currency/BTN').data.decode('utf-8')
    assert 'BHUTAN' in html, 'BTN detail page must show BHUTAN as Country/Region'

def test_btn_detail_not_india(client):
    html = client.get('/currency/BTN').data.decode('utf-8')
    assert 'India' not in html, (
        'BTN detail page must not identify India as its country — '
        'Ngultrum is Bhutan’s currency, not India’s'
    )

def test_lsl_detail_returns_200(client):
    assert client.get('/currency/LSL').status_code == 200

def test_lsl_detail_shows_lesotho(client):
    html = client.get('/currency/LSL').data.decode('utf-8')
    assert 'LESOTHO' in html, 'LSL detail page must show LESOTHO as Country/Region'

def test_lsl_detail_not_south_africa(client):
    html = client.get('/currency/LSL').data.decode('utf-8')
    assert 'South Africa' not in html, (
        'LSL detail page must not identify South Africa as its country — '
        'Loti is Lesotho’s currency, not South Africa’s'
    )

def test_four_records_distinct(client):
    """BTN→Bhutan, INR→India, LSL→Lesotho, ZAR→South Africa — all distinct and correct."""
    data = _load_json()
    assert data['BTN']['country'] == 'BHUTAN',      f"BTN: got {data['BTN']['country']!r}"
    assert data['INR']['country'] == 'India',       f"INR: got {data['INR']['country']!r}"
    assert data['LSL']['country'] == 'LESOTHO',     f"LSL: got {data['LSL']['country']!r}"
    assert data['ZAR']['country'] == 'South Africa',f"ZAR: got {data['ZAR']['country']!r}"

def test_library_ccy_data_btn_is_bhutan(library_html):
    data = _ccy_data_from_html(library_html)
    assert 'BTN' in data, 'BTN not found in CCY_DATA on message-library page'
    assert data['BTN'] == 'BHUTAN', (
        f'CCY_DATA[BTN]: expected "BHUTAN", got {data["BTN"]!r}'
    )

def test_library_ccy_data_btn_not_india(library_html):
    data = _ccy_data_from_html(library_html)
    if 'BTN' in data:
        assert data['BTN'] != 'India', (
            'CCY_DATA[BTN] incorrectly set to India — must be BHUTAN'
        )

def test_library_ccy_data_lsl_is_lesotho(library_html):
    data = _ccy_data_from_html(library_html)
    assert 'LSL' in data, 'LSL not found in CCY_DATA on message-library page'
    assert data['LSL'] == 'LESOTHO', (
        f'CCY_DATA[LSL]: expected "LESOTHO", got {data["LSL"]!r}'
    )

def test_library_ccy_data_lsl_not_south_africa(library_html):
    data = _ccy_data_from_html(library_html)
    if 'LSL' in data:
        assert data['LSL'] != 'South Africa', (
            'CCY_DATA[LSL] incorrectly set to South Africa — must be LESOTHO'
        )

def test_library_ccy_data_inr_is_india(library_html):
    data = _ccy_data_from_html(library_html)
    assert data.get('INR') == 'India', (
        f'CCY_DATA[INR]: expected "India", got {data.get("INR")!r}'
    )

def test_library_ccy_data_zar_is_south_africa(library_html):
    data = _ccy_data_from_html(library_html)
    assert data.get('ZAR') == 'South Africa', (
        f'CCY_DATA[ZAR]: expected "South Africa", got {data.get("ZAR")!r}'
    )


# ── Full JSON ↔ CCY_DATA parity (all codes) ──────────────────────────────────

def test_all_json_codes_present_in_ccy_data(library_html):
    """Every code in currency_codes.json must have a matching row in CCY_DATA."""
    json_data = _load_json()
    ccy_data = _ccy_data_from_html(library_html)
    missing = [code for code in json_data if code not in ccy_data]
    assert not missing, f'Codes in JSON but absent from CCY_DATA: {missing}'


def test_all_ccy_data_codes_present_in_json(library_html):
    """Every code in CCY_DATA must have a backing record in currency_codes.json."""
    json_data = _load_json()
    ccy_data = _ccy_data_from_html(library_html)
    extra = [code for code in ccy_data if code not in json_data]
    assert not extra, f'Codes in CCY_DATA but absent from JSON: {extra}'


def test_full_json_ccy_data_country_parity(library_html):
    """country field in JSON and CCY_DATA must match for every shared code."""
    json_data = _load_json()
    ccy_data = _ccy_data_from_html(library_html)
    mismatches = []
    for code in json_data:
        if code not in ccy_data:
            continue
        j_val = json_data[code]['country']
        c_val = ccy_data[code]
        if j_val != c_val:
            mismatches.append((code, j_val, c_val))
    assert not mismatches, (
        'JSON and CCY_DATA country values disagree:\n' +
        '\n'.join(f'  {c}: JSON={j!r}  CCY_DATA={d!r}' for c, j, d in mismatches)
    )
