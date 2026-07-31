"""Smoke tests: decoder success path and failure path."""
import json
import pytest

# A minimal, deterministic FIX 4.2 Logon message — small and stable
VALID_FIX = '8=FIX.4.2|9=57|35=A|49=CLIENTA|56=BROKRB|34=1|52=20240315-09:29:58.000|98=0|108=30|10=073|'

MALFORMED_INPUTS = [
    '',                     # empty string → status 'empty'
    'not a fix message',    # plain text with no tag=value pairs → 'invalid'
    '!!!===',               # garbage → 'invalid'
    'hello=world|abc=def',  # non-numeric tag numbers → 'invalid'
]


# ---------------------------------------------------------------------------
# Success path
# ---------------------------------------------------------------------------

def test_decoder_success_status(client):
    r = client.post('/decode', data={'fix_message': VALID_FIX})
    assert r.status_code == 200

def test_decoder_success_returns_json(client):
    r = client.post('/decode', data={'fix_message': VALID_FIX})
    data = json.loads(r.data)
    assert data['status'] == 'ok'

def test_decoder_success_has_fields(client):
    r = client.post('/decode', data={'fix_message': VALID_FIX})
    data = json.loads(r.data)
    assert 'fields' in data
    assert len(data['fields']) > 0

def test_decoder_success_contains_known_tag(client):
    r = client.post('/decode', data={'fix_message': VALID_FIX})
    data = json.loads(r.data)
    tags = {f['tag'] for f in data['fields']}
    # Tag 35 (MsgType) must appear in any valid FIX message
    assert 35 in tags

def test_decoder_success_msgtype_is_logon(client):
    r = client.post('/decode', data={'fix_message': VALID_FIX})
    data = json.loads(r.data)
    field_35 = next((f for f in data['fields'] if f['tag'] == 35), None)
    assert field_35 is not None
    assert field_35['value'] == 'A'


# ---------------------------------------------------------------------------
# Failure path — malformed input must never 500
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('bad_input', MALFORMED_INPUTS)
def test_decoder_bad_input_not_500(client, bad_input):
    r = client.post('/decode', data={'fix_message': bad_input})
    assert r.status_code != 500

@pytest.mark.parametrize('bad_input', MALFORMED_INPUTS)
def test_decoder_bad_input_returns_json(client, bad_input):
    r = client.post('/decode', data={'fix_message': bad_input})
    data = json.loads(r.data)
    assert 'status' in data

@pytest.mark.parametrize('bad_input', MALFORMED_INPUTS)
def test_decoder_bad_input_not_ok(client, bad_input):
    r = client.post('/decode', data={'fix_message': bad_input})
    data = json.loads(r.data)
    assert data['status'] != 'ok'
