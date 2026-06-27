import json
import os
from datetime import date as _date

from flask import Flask, render_template, request, jsonify, redirect
from fix_decoder import decode_fix, generate_summary

app = Flask(__name__)

_BASE        = os.path.dirname(__file__)
_THEMES_FILE = os.path.join(_BASE, 'fixreader_data', 'themes.json')
_ACTIVE_FILE = os.path.join(_BASE, 'fixreader_active_theme.json')


# ── Theme engine ─────────────────────────────────────────────

def _load_themes():
    with open(_THEMES_FILE) as f:
        return {t['name']: t for t in json.load(f)}


def _resolve_active_theme(themes):
    """Priority: manual override (today only) > scheduled date > 'default'."""
    today_ymd  = _date.today().isoformat()       # 2026-06-26
    today_mmdd = _date.today().strftime('%m-%d')  # 06-26

    # 1. Manual override — valid only on the day it was set
    try:
        with open(_ACTIVE_FILE) as f:
            data = json.load(f)
        if data.get('manual_date') == today_ymd:
            name = data.get('active_theme', 'default')
            if name in themes:
                return name
    except Exception:
        pass

    # 2. Scheduled theme for today's date
    for theme in themes.values():
        if theme.get('date') == today_mmdd:
            return theme['name']

    return 'default'


def _build_theme_vars(theme):
    colors = theme.get('colors', {})
    if not colors:
        return ''
    lines = ['<style>:root {']
    for var, val in colors.items():
        lines.append(f'  {var}: {val};')
    lines.append('}</style>')
    return '\n'.join(lines)


def _build_theme_info(theme):
    return {
        'name':         theme.get('name', 'default'),
        'display_name': theme.get('display_name', 'Default'),
        'emoji':        theme.get('emoji') or '',
        'subtitle':     theme.get('subtitle') or '',
        'wiki_url':     theme.get('wiki_url') or '',
        'category':     theme.get('category', ''),
        'date':         theme.get('date') or '',
        'type':         theme.get('type') or '',
        'person_name':  theme.get('person_name') or '',
    }


def _ctx(preview=None, **kwargs):
    """Assemble per-request template context: theme vars + display info."""
    themes      = _load_themes()
    render_name = preview if (preview and preview in themes) else _resolve_active_theme(themes)
    theme       = themes.get(render_name) or themes.get('default') or {}
    return {
        'theme_vars':   _build_theme_vars(theme),
        'theme_info':   _build_theme_info(theme),
        'preview_name': preview,
        **kwargs,
    }


def _save_active_theme(name):
    data = {'active_theme': name, 'manual_date': _date.today().isoformat()}
    with open(_ACTIVE_FILE, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')


# ── Stub helper ──────────────────────────────────────────────

def stub(title, description, active_nav=''):
    preview = request.args.get('preview')
    return render_template('stub.html', **_ctx(
        preview=preview,
        page_title=title,
        page_description=description,
        active_nav=active_nav,
    ))


# ── Routes ───────────────────────────────────────────────────

@app.route('/')
def home():
    preview = request.args.get('preview')
    return render_template('index.html', **_ctx(preview=preview))


@app.route('/decode', methods=['POST'])
def decode():
    raw = request.form.get('fix_message', '').strip()
    fields, status = decode_fix(raw)
    if status == 'ok' and fields:
        summary = generate_summary(fields)
        return jsonify({'status': 'ok', 'fields': fields, 'summary': summary})
    return jsonify({'status': status})


@app.route('/themes-admin')
def themes_admin():
    preview  = request.args.get('preview')
    themes   = _load_themes()
    active   = _resolve_active_theme(themes)
    sorted_themes = sorted(
        themes.values(),
        key=lambda t: t.get('date') or 'zz-zz',  # no date → sorts last
    )
    return render_template('themes_admin.html', **_ctx(
        preview=preview,
        themes_list=sorted_themes,
        active_theme_name=active,
        preview_theme_info=themes.get(preview) if preview else None,
    ))


@app.route('/themes-admin/apply', methods=['POST'])
def themes_admin_apply():
    name   = request.form.get('theme', 'default')
    themes = _load_themes()
    if name in themes:
        _save_active_theme(name)
    return redirect('/themes-admin')


@app.route('/themes-admin/edit', methods=['POST'])
def themes_admin_edit():
    import re
    data = request.get_json(force=True) or {}
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'status': 'error', 'message': 'Missing theme name'}), 400

    with open(_THEMES_FILE) as f:
        themes_list = json.load(f)

    theme = next((t for t in themes_list if t['name'] == name), None)
    if not theme:
        return jsonify({'status': 'error', 'message': 'Theme not found'}), 404

    for field in ('display_name', 'subtitle', 'emoji', 'wiki_url'):
        if field in data:
            theme[field] = data[field] or None

    hex_re = re.compile(r'^#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?$')
    if isinstance(data.get('colors'), dict):
        existing = theme.get('colors', {})
        for var, val in data['colors'].items():
            if var in existing and hex_re.match(str(val)):
                existing[var] = val

    with open(_THEMES_FILE, 'w') as f:
        json.dump(themes_list, f, indent=2)
        f.write('\n')

    return jsonify({'status': 'ok'})


@app.route('/compare')
def compare():
    return stub(
        'Compare Messages',
        'Paste two FIX messages side by side and see a diff — identical tags in grey, '
        'changed values highlighted, missing tags flagged. Great for debugging order '
        'state transitions and spotting what changed between an original order and a cancel/replace.',
        'compare',
    )


@app.route('/learn')
def learn():
    return stub(
        'Learn FIX',
        'A structured curriculum for understanding FIX Protocol from the ground up — '
        'message types, session management, order flows, and field-by-field breakdowns '
        'across FIX 4.0 through FIXT 1.1.',
        'learn',
    )


@app.route('/interview-prep')
def interview_prep():
    return stub(
        'Interview Prep',
        '153 Q&A covering everything from session-level concepts to complex order routing. '
        'Practice with mock interviews, common scenario walkthroughs, and a printable '
        'FIX cheat sheet built for trading technology roles.',
        'interview-prep',
    )


@app.route('/tools')
def tools():
    return stub(
        'Tools',
        'A suite of FIX utilities in one place — build messages from scratch, validate '
        'tag compliance, diff two messages side by side, or decode straight from a log '
        'file. Everything you need without leaving the browser.',
        'tools',
    )


@app.route('/library')
@app.route('/message-library')
def message_library():
    return stub(
        'Message Library',
        'A searchable reference of real-world FIX messages across every message type. '
        'See how New Orders, Execution Reports, session messages, and post-trade '
        'confirmations look in practice — with annotated tag-by-tag breakdowns.',
        'library',
    )


@app.route('/resources')
def resources():
    return stub(
        'Resources',
        'FIX Protocol specs, vendor documentation, open-source libraries, and community '
        'links — everything you need to go deeper on FIX development, integration work, '
        'or certification prep.',
        'resources',
    )


@app.route('/about')
def about():
    return stub(
        'About FIXReader',
        'FIXReader is a free, open-source tool built for traders, developers, and anyone '
        'who works with FIX Protocol. No login, no tracking — just fast, accurate message '
        'decoding and a growing library of FIX learning resources.',
        'about',
    )


@app.route('/field-reference')
@app.route('/reference')
def field_reference():
    return stub(
        'Field Reference',
        'Every FIX tag, in one place. Search by tag number or name, filter by message '
        'type, and see valid values, data types, and examples — covering FIX 4.0 through '
        'FIXT 1.1 across all 1,102 defined tags.',
        'field-reference',
    )


@app.route('/tag-validator')
@app.route('/validator')
def tag_validator():
    return stub(
        'Tag Validator',
        'Paste a FIX message and check it against the spec — required tags, valid values, '
        'sequence rules, and message-type constraints all flagged in one pass. Catch '
        'issues before they hit a counterparty.',
        'tag-validator',
    )


@app.route('/message-builder')
@app.route('/builder')
def message_builder():
    return stub(
        'Message Builder',
        'Build valid FIX messages from scratch. Select a message type, fill in required '
        'fields, and export the result as a raw FIX string or JSON — with real-time '
        'validation as you go.',
        'message-builder',
    )


if __name__ == '__main__':
    app.run(debug=True)
