"""Smoke tests: theme-admin production guard."""
import os
import pytest


# ---------------------------------------------------------------------------
# Theme-admin guard — all three endpoints must return 404 when env var unset
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def clear_theme_admin_env(monkeypatch):
    """Ensure ENABLE_THEME_ADMIN is absent for every test in this module."""
    monkeypatch.delenv('ENABLE_THEME_ADMIN', raising=False)


def test_themes_admin_get_404(client):
    r = client.get('/themes-admin')
    assert r.status_code == 404

def test_themes_admin_apply_post_404(client):
    r = client.post('/themes-admin/apply')
    assert r.status_code == 404

def test_themes_admin_edit_post_404(client):
    r = client.post('/themes-admin/edit')
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Theme-admin enabled — confirm routes become accessible
# ---------------------------------------------------------------------------

def test_themes_admin_enabled_get_200(client, monkeypatch):
    monkeypatch.setenv('ENABLE_THEME_ADMIN', 'true')
    r = client.get('/themes-admin')
    assert r.status_code == 200

def test_themes_admin_enabled_apply_redirects(client, monkeypatch):
    monkeypatch.setenv('ENABLE_THEME_ADMIN', 'true')
    r = client.post('/themes-admin/apply', data={'theme': 'default'})
    # apply always redirects back to /themes-admin
    assert r.status_code in (301, 302)
