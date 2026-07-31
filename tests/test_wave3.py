"""Wave 3 — editorial quality, terminology consistency, and content accuracy tests."""
import pytest
import os


# ---------------------------------------------------------------------------
# Task 1: Editorial corrections
# ---------------------------------------------------------------------------

def test_index_empty_state_cta_no_popular_topics(client):
    r = client.get('/')
    html = r.data.decode('utf-8')
    assert 'Popular Topics' not in html


def test_gap_fill_badge_is_gap_not_rsd(client):
    r = client.get('/troubleshooting/gap-fill')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    # Badge must be GAP (matching sidebar code)
    assert '>GAP<' in html
    # RSD must not appear as a badge
    assert '>RSD<' not in html


def test_logon_required_fields_table_tag_35_not_35_equals_a(client):
    r = client.get('/troubleshooting/logon')
    html = r.data.decode('utf-8')
    # Tag column must show "35" not "35=A"
    assert '<td class="mono">35</td>' in html
    # The value "A" should appear in the description, not the tag column
    assert '35=A' not in html.split('<td class="mono">35</td>')[0].split('<tbody>')[-1]


def test_logon_5min_diagnosis_no_sentence_fragment(client):
    r = client.get('/troubleshooting/logon')
    html = r.data.decode('utf-8')
    # Fragment "Network, configuration, or sequence?" must not appear
    assert 'Network, configuration, or sequence?' not in html
    # Vague "reset" without context must not appear
    assert "Only reset after you've proven recovery isn't possible." not in html


def test_network_page_desc_uses_imperative(client):
    r = client.get('/troubleshooting/network')
    html = r.data.decode('utf-8')
    # "Diagnosing" (gerund form) must not be the page intro
    assert 'Diagnosing FIX TCP connection failures' not in html
    # Imperative form is used
    assert 'Diagnose FIX TCP connection failures' in html


def test_resources_box_options_not_xbox(client):
    r = client.get('/resources')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    # BOX Options Exchange abbreviation must be BOX, not XBOX
    assert '(XBOX)' not in html
    assert '(BOX)' in html


def test_resources_memx_no_recently(client):
    r = client.get('/resources')
    html = r.data.decode('utf-8')
    assert 'Recently launched' not in html
    assert 'Launched 2023' in html


def test_resources_has_fix_protocol_standards_section(client):
    r = client.get('/resources')
    html = r.data.decode('utf-8')
    assert 'FIX Protocol Standards' in html


def test_cert_allocation_subtitle_count_37(client):
    r = client.get('/cert/allocation')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    assert '37 tests across 5 phases' in html
    assert '38 tests across 5 phases' not in html


# ---------------------------------------------------------------------------
# Task 2: Terminology standardization
# ---------------------------------------------------------------------------

def test_message_library_enumeration_values_not_enum(client):
    r = client.get('/message-library')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    assert 'Appendix — Enumeration Values' in html
    assert 'Appendix — Enum Values' not in html


def test_fix_reference_enumeration_values_not_enum(client):
    r = client.get('/reference/fix42')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    assert 'Appendix — Enumeration Values' in html
    assert 'Appendix — Enum Values' not in html


def test_sequence_no_resendrequest_one_word_in_prose(client):
    r = client.get('/troubleshooting/sequence-numbers')
    html = r.data.decode('utf-8')
    # "Resend Request" (two words) must appear as a heading
    assert 'Resend Request' in html
    # "ResendRequest" as one word must only appear in code blocks (log output)
    # Verify the table uses two-word form
    assert '<strong>Resend Request</strong>' in html


def test_sequence_checksum_placeholder_not_xxx(client):
    r = client.get('/troubleshooting/sequence-numbers')
    html = r.data.decode('utf-8')
    assert '10=xxx' not in html
    assert '10=000' in html


def test_network_section_headings_no_ampersand(client):
    r = client.get('/troubleshooting/network')
    html = r.data.decode('utf-8')
    # Section headings should use "and" not "&"
    assert 'Heartbeat and TestRequest Diagnostics' in html
    assert 'Logon Sequence and Timeout' in html
    assert 'Firewall and Port Configuration' in html
    assert 'SSL/TLS Configuration' in html
    # Verify old forms are gone
    assert 'Heartbeat &amp; TestRequest Diagnostics' not in html
    assert 'SSL / TLS Configuration' not in html


def test_no_british_spelling_acknowledgement_in_templates():
    # Check template source files directly — the rendered HTML may include
    # "Quote Acknowledgement" from fix_tags.json (official FIX message name)
    # which we must not change, but template prose should use American spelling.
    import os
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    templates_to_check = [
        'troubleshooting_latency.html',
        'cert_order_entry.html',
        'cert_drop_copy.html',
        'cert_allocation.html',
    ]
    for fname in templates_to_check:
        path = os.path.join(template_dir, fname)
        with open(path) as f:
            content = f.read()
        assert 'acknowledgement' not in content, (
            f"British spelling 'acknowledgement' found in template {fname}"
        )


def test_cert_drop_copy_possduplication_corrected(client):
    r = client.get('/cert/drop-copy')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    # Redundant "PossDupFlag=Y, Tag 43=Y" must not appear
    assert 'PossDupFlag=Y, Tag 43=Y' not in html
    # Correct form
    assert 'PossDupFlag (43) = Y' in html


def test_cert_allocation_resend_request_two_words(client):
    r = client.get('/cert/allocation')
    html = r.data.decode('utf-8')
    assert 'Resend Request (35=2)' in html


def test_cert_drop_copy_resend_request_two_words(client):
    r = client.get('/cert/drop-copy')
    html = r.data.decode('utf-8')
    assert 'Resend Request (35=2)' in html


# ---------------------------------------------------------------------------
# Task 1+2: Technical accuracy corrections
# ---------------------------------------------------------------------------

def test_fill_reconciliation_exectype_version_aware(client):
    r = client.get('/troubleshooting/fill-reconciliation')
    html = r.data.decode('utf-8')
    # Must show both FIX 4.2 and FIX 4.4+ ExecType values
    assert 'FIX 4.2' in html
    assert 'FIX 4.4+' in html
    # ExecType=2 (Fill in FIX 4.2) must be present
    assert '<code>2</code>' in html
    # Old inaccurate description must not appear
    assert "'F' = fill, '1' = partial fill" not in html


def test_troubleshooting_order_rejects_heading_no_first_question(client):
    r = client.get('/troubleshooting/rejects')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    assert 'First Question:' not in html
    assert 'What Rejected the Order?' in html


def test_troubleshooting_duplicate_orders_possdup_full_form(client):
    r = client.get('/troubleshooting/duplicate-orders')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    # Truncated "PossDup" without tag number must not appear in prose
    assert '>PossDup<' not in html
    assert 'PossDupFlag (43)' in html


# ---------------------------------------------------------------------------
# Task 2: Style guide exists
# ---------------------------------------------------------------------------

def test_style_guide_file_exists():
    path = os.path.join(
        os.path.dirname(__file__), '..', 'STYLE_GUIDE.md'
    )
    assert os.path.isfile(path), "STYLE_GUIDE.md must exist at project root"


def test_style_guide_covers_key_terms():
    path = os.path.join(
        os.path.dirname(__file__), '..', 'STYLE_GUIDE.md'
    )
    with open(path) as f:
        content = f.read()
    # Must document the key terminology decisions
    assert 'Resend Request' in content
    assert 'acknowledgment' in content
    assert 'Enumeration Values' in content
    assert 'ResetSeqNumFlag' in content
    assert 'ExecType' in content


# ---------------------------------------------------------------------------
# Cross-link and route integrity
# ---------------------------------------------------------------------------

def test_all_troubleshooting_routes_200(client):
    routes = [
        '/troubleshooting/network',
        '/troubleshooting/sequence-numbers',
        '/troubleshooting/logon',
        '/troubleshooting/fill-reconciliation',
        '/troubleshooting/rejects',
        '/troubleshooting/latency',
        '/troubleshooting/duplicate-orders',
        '/troubleshooting/gap-fill',
    ]
    for route in routes:
        r = client.get(route)
        assert r.status_code == 200, f"Route {route} returned {r.status_code}"


def test_cert_routes_200(client):
    routes = ['/cert/order-entry', '/cert/drop-copy', '/cert/allocation']
    for route in routes:
        r = client.get(route)
        assert r.status_code == 200, f"Route {route} returned {r.status_code}"
