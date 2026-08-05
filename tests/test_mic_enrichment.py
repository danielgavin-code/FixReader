"""Tests for MIC enrichment infrastructure.

Verifies: enrichment file is valid JSON; all keys are real MICs;
a MIC with no enrichment renders cleanly; a MIC with a partial entry
renders only its populated fields.
"""
import json
import os
import pytest

import app as app_module


_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fixreader_data')
_ENRICHMENT_PATH = os.path.join(_DATA_DIR, 'mic_enrichment.json')
_MIC_CODES_PATH = os.path.join(_DATA_DIR, 'mic_codes.json')


def test_enrichment_file_is_valid_json():
    with open(_ENRICHMENT_PATH) as f:
        data = json.load(f)
    assert isinstance(data, dict)


def test_enrichment_keys_match_real_mics():
    with open(_MIC_CODES_PATH) as f:
        real_mics = {m['mic'] for m in json.load(f)}
    with open(_ENRICHMENT_PATH) as f:
        enrichment = json.load(f)
    unknown = set(enrichment.keys()) - real_mics
    assert not unknown, f"Keys in mic_enrichment.json not found in mic_codes.json: {unknown}"


def test_mic_without_enrichment_renders_cleanly(client):
    r = client.get('/mic/XNYS')
    assert r.status_code == 200
    html = r.data.decode()
    assert 'XNYS' in html
    # Enrichment sections must not be rendered when there is no enrichment entry
    assert '<div class="mic-detail-card mic-enrichment-section">' not in html
    assert '<ul class="mic-sources-list">' not in html


def test_mic_with_partial_enrichment_renders_only_populated_fields(client, monkeypatch):
    partial = {
        'legal_entity': 'New York Stock Exchange LLC',
        'website': 'https://www.nyse.com',
        'sources': [
            {'title': 'NYSE FIX Specification', 'url': 'https://www.nyse.com/fix', 'retrieved': '2026-08-05'}
        ],
    }
    monkeypatch.setattr(app_module, '_get_mic_enrichment', lambda _: partial)

    r = client.get('/mic/XNYS')
    assert r.status_code == 200
    html = r.data.decode()

    # Populated fields appear
    assert 'New York Stock Exchange LLC' in html
    assert 'https://www.nyse.com' in html
    assert 'NYSE FIX Specification' in html
    assert 'Retrieved 2026-08-05' in html

    # Unpopulated fields do not appear
    assert 'Parent Company' not in html
    assert 'Headquarters' not in html
    assert 'Institution Type' not in html
