"""Wave 4 — core tool enhancements: input handling, output improvements, validator diagnostics,
builder message types, and curated example messages."""
import pytest
import os


# ---------------------------------------------------------------------------
# Task 1: Decoder input handling — caret-A (^A) delimiter support
# ---------------------------------------------------------------------------

def test_decode_caret_a_delimiter(client):
    """^A literal notation is accepted as a field delimiter."""
    msg = '8=FIX.4.2^A9=82^A35=A^A49=CLIENTA^A56=BROKRB^A34=1^A52=20240315-09:29:58.000^A98=0^A108=30^A10=073^A'
    r = client.post('/decode', data={'fix_message': msg})
    assert r.status_code == 200
    data = r.get_json()
    assert data['status'] == 'ok'
    fields = {f['tag']: f['value'] for f in data['fields']}
    assert fields[35] == 'A'
    assert fields[49] == 'CLIENTA'
    assert fields[108] == '30'


def test_decode_caret_a_in_log_prefix(client):
    """^A delimiter is handled even when preceded by a log prefix."""
    msg = '2024-03-15 09:30:00.123 OUT 8=FIX.4.2^A9=57^A35=0^A49=ACME^A56=NYSE^A34=5^A52=20240315-09:30:00.000^A10=001^A'
    r = client.post('/decode', data={'fix_message': msg})
    assert r.status_code == 200
    data = r.get_json()
    assert data['status'] == 'ok'
    fields = {f['tag']: f['value'] for f in data['fields']}
    assert fields[35] == '0'


def test_decode_mixed_delimiter_pipe_preferred(client):
    """Pipe-delimited messages decode correctly when no SOH/^A present."""
    msg = '8=FIX.4.2|9=73|35=A|49=ACME|56=NYSE|34=1|52=20060324-17:44:59|98=0|108=30|141=Y|10=063|'
    r = client.post('/decode', data={'fix_message': msg})
    assert r.status_code == 200
    data = r.get_json()
    assert data['status'] == 'ok'
    fields = {f['tag']: f['value'] for f in data['fields']}
    assert fields[35] == 'A'


def test_decode_soh_delimiter(client):
    """SOH-delimited messages (actual \x01) decode correctly."""
    msg = '8=FIX.4.2\x019=73\x0135=A\x0149=ACME\x0156=NYSE\x0134=1\x0152=20060324-17:44:59\x0198=0\x01108=30\x0110=063\x01'
    r = client.post('/decode', data={'fix_message': msg})
    assert r.status_code == 200
    data = r.get_json()
    assert data['status'] == 'ok'
    fields = {f['tag']: f['value'] for f in data['fields']}
    assert fields[35] == 'A'


def test_decode_log_prefix_with_direction(client):
    """Direction prefixes (IN/OUT) before a FIX message are stripped."""
    msg = 'OUT 8=FIX.4.2|9=57|35=0|49=ACME|56=NYSE|34=12|52=20060324-17:50:00|10=110|'
    r = client.post('/decode', data={'fix_message': msg})
    assert r.status_code == 200
    data = r.get_json()
    assert data['status'] == 'ok'
    fields = {f['tag']: f['value'] for f in data['fields']}
    assert fields[35] == '0'


# ---------------------------------------------------------------------------
# Task 2: Decoder output — CSV export button, required field marking
# ---------------------------------------------------------------------------

def test_decoder_has_csv_export_button(client):
    r = client.get('/')
    html = r.data.decode('utf-8')
    assert 'id="btn-export-csv"' in html


def test_decoder_no_excel_export_button(client):
    """Excel export button removed — dead UI replaced with working CSV only."""
    r = client.get('/')
    html = r.data.decode('utf-8')
    assert 'btn-export-xlsx' not in html


def test_decoder_no_dead_copy_raw_js(client):
    """Dead #copy-raw element reference removed from decoder JS."""
    r = client.get('/')
    html = r.data.decode('utf-8')
    assert "getElementById('copy-raw')" not in html


def test_decoder_req_dot_checks_body_fields(client):
    """reqDot() checks body required fields via fix_tags.json required_in."""
    r = client.get('/')
    html = r.data.decode('utf-8')
    # reqDot now accepts a msgType argument — check the updated function signature
    assert 'function reqDot(f, msgType)' in html
    # reqDot checks required_in for body fields
    assert 'required_in' in html
    assert "ri.code === msgType" in html


# ---------------------------------------------------------------------------
# Task 3: Validator diagnostics — ^A support, duplicate detection, ordering
# ---------------------------------------------------------------------------

def test_validator_caret_a_support_in_js(client):
    r = client.get('/tools/tag-validator')
    html = r.data.decode('utf-8')
    # _stripLogPrefix now normalizes ^A
    assert r'replace(/\^A/g' in html or "replace(/\\^A/g" in html


def test_validator_duplicate_detection_in_js(client):
    r = client.get('/tools/tag-validator')
    html = r.data.decode('utf-8')
    assert 'isDuplicate' in html
    assert 'Duplicate' in html


def test_validator_ordering_check_in_js(client):
    r = client.get('/tools/tag-validator')
    html = r.data.decode('utf-8')
    assert 'BeginString' in html
    assert 'must be first' in html


def test_validator_has_more_samples(client):
    r = client.get('/tools/tag-validator')
    html = r.data.decode('utf-8')
    # All these samples must be present in VAL_SAMPLES
    assert 'test_request' in html
    assert 'resend_request' in html
    assert 'sequence_reset' in html
    assert 'cancel_reject' in html
    assert 'heartbeat' in html
    assert 'logout' in html


def test_validator_dropdown_has_new_examples(client):
    r = client.get('/tools/tag-validator')
    html = r.data.decode('utf-8')
    assert "valExLoad('test_request')" in html
    assert "valExLoad('resend_request')" in html
    assert "valExLoad('sequence_reset')" in html
    assert "valExLoad('cancel_reject')" in html
    assert "valExLoad('heartbeat')" in html
    assert "valExLoad('logout')" in html


# ---------------------------------------------------------------------------
# Task 4: Builder — new message types and round-trip button
# ---------------------------------------------------------------------------

def test_builder_has_sequence_reset(client):
    r = client.get('/tools/message-builder')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    assert 'value="4"' in html
    assert 'Sequence Reset' in html


def test_builder_has_order_cancel_reject(client):
    r = client.get('/tools/message-builder')
    html = r.data.decode('utf-8')
    assert 'value="9"' in html
    assert 'Order Cancel Reject' in html


def test_builder_has_business_message_reject(client):
    r = client.get('/tools/message-builder')
    html = r.data.decode('utf-8')
    assert 'value="j"' in html
    assert 'Business Message Reject' in html


def test_builder_has_send_to_decoder_button(client):
    r = client.get('/tools/message-builder')
    html = r.data.decode('utf-8')
    assert 'bldSendToDecoder' in html


def test_builder_caret_a_in_load(client):
    r = client.get('/tools/message-builder')
    html = r.data.decode('utf-8')
    assert r'replace(/\^A/g' in html or "replace(/\\^A/g" in html


# ---------------------------------------------------------------------------
# Task 5: Decoder example messages expanded
# ---------------------------------------------------------------------------

def test_decoder_has_test_request_sample(client):
    r = client.get('/')
    html = r.data.decode('utf-8')
    assert 'test_request' in html
    assert '35=1' in html


def test_decoder_has_resend_request_sample(client):
    r = client.get('/')
    html = r.data.decode('utf-8')
    assert 'resend_request' in html
    assert '35=2' in html


def test_decoder_has_sequence_reset_sample(client):
    r = client.get('/')
    html = r.data.decode('utf-8')
    assert 'sequence_reset' in html
    assert '35=4' in html


def test_decoder_has_cancel_reject_sample(client):
    r = client.get('/')
    html = r.data.decode('utf-8')
    assert 'cancel_reject' in html
    assert '35=9' in html


def test_decoder_examples_dropdown_has_new_entries(client):
    r = client.get('/')
    html = r.data.decode('utf-8')
    assert 'data-msg="test_request"' in html
    assert 'data-msg="resend_request"' in html
    assert 'data-msg="sequence_reset"' in html
    assert 'data-msg="cancel_reject"' in html


# ---------------------------------------------------------------------------
# Regression: all tool routes still return 200
# ---------------------------------------------------------------------------

def test_all_tool_routes_200(client):
    for route in ['/', '/tools/message-builder', '/tools/tag-validator', '/compare']:
        r = client.get(route)
        assert r.status_code == 200, f"Route {route} returned {r.status_code}"


# ---------------------------------------------------------------------------
# Functional: decode the new example messages end-to-end
# ---------------------------------------------------------------------------

def test_decode_test_request_end_to_end(client):
    msg = '8=FIX.4.2|9=75|35=1|49=CLIENTA|56=BROKRB|34=12|52=20240315-09:35:00.000|112=TESTREQ-001|10=031|'
    r = client.post('/decode', data={'fix_message': msg})
    data = r.get_json()
    assert data['status'] == 'ok'
    assert data['summary']['msg_type_val'] == '1'
    assert data['summary']['msg_type_name'] == 'Test Request'


def test_decode_resend_request_end_to_end(client):
    msg = '8=FIX.4.2|9=67|35=2|49=CLIENTA|56=BROKRB|34=13|52=20240315-09:36:00.000|7=5|16=0|10=188|'
    r = client.post('/decode', data={'fix_message': msg})
    data = r.get_json()
    assert data['status'] == 'ok'
    assert data['summary']['msg_type_val'] == '2'
    assert data['summary']['msg_type_name'] == 'Resend Request'


def test_decode_sequence_reset_end_to_end(client):
    msg = '8=FIX.4.2|9=74|35=4|49=BROKRB|56=CLIENTA|34=1|52=20240315-09:37:00.000|123=Y|36=20|10=155|'
    r = client.post('/decode', data={'fix_message': msg})
    data = r.get_json()
    assert data['status'] == 'ok'
    assert data['summary']['msg_type_val'] == '4'
    assert data['summary']['msg_type_name'] == 'Sequence Reset'


def test_decode_order_cancel_reject_end_to_end(client):
    msg = '8=FIX.4.2|9=155|35=9|49=BROKRB|56=CLIENTA|34=5|52=20240315-09:45:05.000|11=CXL-001|37=BRKORD-001|39=2|41=ORD-001|434=1|58=Order already filled|10=177|'
    r = client.post('/decode', data={'fix_message': msg})
    data = r.get_json()
    assert data['status'] == 'ok'
    assert data['summary']['msg_type_val'] == '9'
    assert data['summary']['msg_type_name'] == 'Order Cancel Reject'
