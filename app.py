import json
import os
from datetime import date as _date

from flask import Flask, render_template, request, jsonify, redirect, abort
from fix_decoder import decode_fix, generate_summary

app = Flask(__name__)

_BASE        = os.path.dirname(__file__)
_THEMES_FILE = os.path.join(_BASE, 'fixreader_data', 'themes.json')
_TAGS_FILE   = os.path.join(_BASE, 'fixreader_data', 'fix_tags.json')
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


_SAMPLES = {
    # Order Messages
    'new_order_single': (
        '8=FIX.4.2|9=162|35=D|49=CLIENTA|56=BROKRB|34=1|52=20240315-09:30:00.000|'
        '11=ORD-001|21=1|55=AAPL|54=1|38=500|40=2|44=178.50|59=0|60=20240315-09:30:00.000|10=128|'
    ),
    'order_cancel_request': (
        '8=FIX.4.2|9=148|35=F|49=CLIENTA|56=BROKRB|34=5|52=20240315-09:45:00.000|'
        '11=CXL-001|41=ORD-001|55=AAPL|54=1|38=500|60=20240315-09:45:00.000|10=054|'
    ),
    'order_cancel_replace': (
        '8=FIX.4.2|9=175|35=G|49=CLIENTA|56=BROKRB|34=3|52=20240315-09:33:00.000|'
        '11=REP-001|41=ORD-001|55=AAPL|54=1|38=300|40=2|44=179.00|59=0|60=20240315-09:33:00.000|10=089|'
    ),
    'order_status_request': (
        '8=FIX.4.2|9=114|35=H|49=CLIENTA|56=BROKRB|34=4|52=20240315-09:35:00.000|'
        '37=BRKORD-001|11=ORD-001|55=AAPL|54=1|10=201|'
    ),
    'order_cancel_reject': (
        '8=FIX.4.2|9=155|35=9|49=BROKRB|56=CLIENTA|34=5|52=20240315-09:45:05.000|'
        '11=CXL-001|37=BRKORD-001|39=2|41=ORD-001|434=1|58=Order already filled|10=177|'
    ),
    # Execution Reports
    'exec_report_new': (
        '8=FIX.4.2|9=222|35=8|49=BROKRB|56=CLIENTA|34=2|52=20240315-09:30:00.100|'
        '11=ORD-001|17=EXEC-001|37=BRKORD-001|150=0|39=0|55=AAPL|54=1|38=500|40=2|44=178.50|'
        '32=0|31=0.00|151=500|14=0|6=0.00|60=20240315-09:30:00.100|10=033|'
    ),
    'exec_report_partial': (
        '8=FIX.4.2|9=233|35=8|49=BROKRB|56=CLIENTA|34=3|52=20240315-09:31:15.000|'
        '11=ORD-001|17=EXEC-002|37=BRKORD-001|150=1|39=1|55=AAPL|54=1|38=500|40=2|44=178.50|'
        '32=200|31=178.48|151=300|14=200|6=178.48|60=20240315-09:31:15.000|10=211|'
    ),
    'exec_report_fill': (
        '8=FIX.4.2|9=234|35=8|49=BROKRB|56=CLIENTA|34=4|52=20240315-09:31:45.000|'
        '11=ORD-001|17=EXEC-003|37=BRKORD-001|150=2|39=2|55=AAPL|54=1|38=500|40=2|44=178.50|'
        '32=300|31=178.47|151=0|14=500|6=178.48|60=20240315-09:31:45.000|10=199|'
    ),
    'exec_report_cancelled': (
        '8=FIX.4.2|9=225|35=8|49=BROKRB|56=CLIENTA|34=6|52=20240315-09:45:05.100|'
        '11=CXL-001|17=EXEC-004|37=BRKORD-001|150=4|39=4|55=AAPL|54=1|38=500|40=2|44=178.50|'
        '32=0|31=0.00|151=0|14=0|6=0.00|60=20240315-09:45:05.100|10=144|'
    ),
    'exec_report_replaced': (
        '8=FIX.4.2|9=228|35=8|49=BROKRB|56=CLIENTA|34=7|52=20240315-09:33:30.000|'
        '11=REP-001|17=EXEC-005|37=BRKORD-002|150=5|39=5|55=AAPL|54=1|38=300|40=2|44=179.00|'
        '32=0|31=0.00|151=300|14=0|6=0.00|60=20240315-09:33:30.000|10=018|'
    ),
    'exec_report_rejected': (
        '8=FIX.4.2|9=200|35=8|49=BROKRB|56=CLIENTA|34=8|52=20240315-09:30:00.500|'
        '11=BAD-001|17=EXEC-006|37=NONE|150=8|39=8|55=INVALID|54=1|38=100|40=2|44=0.00|'
        '32=0|31=0.00|151=0|14=0|6=0.00|58=Unknown symbol|10=077|'
    ),
    # Session Messages
    'logon': (
        '8=FIX.4.2|9=82|35=A|49=CLIENTA|56=BROKRB|34=1|52=20240315-09:29:58.000|'
        '98=0|108=30|10=073|'
    ),
    'heartbeat': (
        '8=FIX.4.2|9=57|35=0|49=BROKRB|56=CLIENTA|34=15|52=20240315-09:30:00.000|10=202|'
    ),
    'test_request': (
        '8=FIX.4.2|9=75|35=1|49=CLIENTA|56=BROKRB|34=12|52=20240315-09:35:00.000|'
        '112=TESTREQ-001|10=031|'
    ),
    'resend_request': (
        '8=FIX.4.2|9=67|35=2|49=CLIENTA|56=BROKRB|34=13|52=20240315-09:36:00.000|'
        '7=5|16=0|10=188|'
    ),
    'reject': (
        '8=FIX.4.2|9=114|35=3|49=BROKRB|56=CLIENTA|34=14|52=20240315-09:30:02.000|'
        '45=1|371=38|372=D|373=5|58=Required tag missing|10=099|'
    ),
    'sequence_reset': (
        '8=FIX.4.2|9=74|35=4|49=BROKRB|56=CLIENTA|34=1|52=20240315-09:37:00.000|'
        '123=Y|36=20|10=155|'
    ),
    'logout': (
        '8=FIX.4.2|9=76|35=5|49=CLIENTA|56=BROKRB|34=20|52=20240315-09:40:00.000|'
        '58=Goodbye|10=211|'
    ),
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
    try:
        with open(_TAGS_FILE) as f:
            tag_ref = {str(t['tag']): t for t in json.load(f)}
    except Exception:
        tag_ref = {}
    return render_template('index.html', **_ctx(preview=preview),
                           tag_ref_json=json.dumps(tag_ref),
                           sample_messages_json=json.dumps(_SAMPLES))


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
    with open(_TAGS_FILE) as f:
        tag_list = json.load(f)
    return render_template('compare.html',
                           tag_list_json=json.dumps(tag_list),
                           **_ctx(preview=request.args.get('preview')))


@app.route('/learn')
def learn():
    return stub(
        'Learn FIX',
        'A structured curriculum for understanding FIX Protocol from the ground up — '
        'message types, session management, order flows, and field-by-field breakdowns '
        'across FIX 4.0 through FIXT 1.1.',
        'learn',
    )


@app.route('/troubleshooting')
@app.route('/troubleshooting/<path:subpath>')
def troubleshooting(subpath=None):
    titles = {
        'network': 'Network & Connectivity',
        'sequence-numbers': 'Sequence Number Issues',
        'logon': 'Logon Failures',
        'fill-reconciliation': 'Fill Reconciliation',
        'rejects': 'Order Rejects',
        'latency': 'Latency & Timing',
        'duplicate-orders': 'Duplicate Orders',
        'gap-fill': 'Gap Fill & Resend',
    }
    title = titles.get(subpath, 'Troubleshooting')
    return render_template('stub.html', **_ctx(
        page_title=title,
        page_description=f'FIX Protocol troubleshooting guide: {title}.',
        active_nav='troubleshooting',
    ))


@app.route('/tools')
def tools():
    return redirect('/')


@app.route('/library')
@app.route('/message-library')
def message_library():
    preview = request.args.get('preview')
    with open(_TAGS_FILE) as f:
        tag_list = json.load(f)
    return render_template('message_library.html',
                           tag_list_json=json.dumps(tag_list),
                           **_ctx(preview=preview))


@app.route('/exchange-specs')
def exchange_specs():
    return render_template('exchange_specs.html', **_ctx())


_VERSION_ORDER = [
    'FIX 2.7', 'FIX 4.0', 'FIX 4.1', 'FIX 4.2', 'FIX 4.3',
    'FIX 4.4', 'FIX 5.0', 'FIX 5.0 SP1', 'FIX 5.0 SP2', 'FIXT 1.1',
]

_VERSION_MAP = {
    'fix40':    {'name': 'FIX 4.0',     'version_key': 'FIX 4.0',     'withdrawn': False},
    'fix41':    {'name': 'FIX 4.1',     'version_key': 'FIX 4.1',     'withdrawn': False},
    'fix42':    {'name': 'FIX 4.2',     'version_key': 'FIX 4.2',     'withdrawn': False},
    'fix43':    {'name': 'FIX 4.3',     'version_key': 'FIX 4.3',     'withdrawn': True},
    'fix44':    {'name': 'FIX 4.4',     'version_key': 'FIX 4.4',     'withdrawn': False},
    'fix50':    {'name': 'FIX 5.0',     'version_key': 'FIX 5.0',     'withdrawn': False},
    'fix50sp1': {'name': 'FIX 5.0 SP1', 'version_key': 'FIX 5.0 SP1', 'withdrawn': False},
    'fix50sp2': {'name': 'FIX 5.0 SP2', 'version_key': 'FIX 5.0 SP2', 'withdrawn': False},
}

_SESSION_CODES  = {'All', 'A', '0', '1', '2', '3', '4', '5', 'j'}
_ORDER_CODES    = {'D', 'E', 'F', 'G', 'H'}
_EXEC_CODES     = {'8', '9'}
_POSTTRADE_CODES = {'J', 'P', 'Q', 'AE', 'AF', 'AP', 'AS', 'AV', 'AW'}


def _tag_category(tag):
    codes = set()
    for m in tag.get('required_in', []):
        codes.add(m['code'])
    for m in tag.get('optional_in', []):
        codes.add(m['code'])
    if codes & _SESSION_CODES:
        return 'session'
    if codes & _POSTTRADE_CODES and not (codes & _ORDER_CODES or codes & _EXEC_CODES):
        return 'posttrade'
    if codes & _EXEC_CODES and not codes & _ORDER_CODES:
        return 'execution'
    if codes & _ORDER_CODES:
        return 'order'
    return 'other'


@app.route('/reference/<version>')
def tag_reference_page(version):
    if version not in _VERSION_MAP:
        abort(404)
    ver_info = _VERSION_MAP[version]
    v_idx = _VERSION_ORDER.index(ver_info['version_key'])
    with open(_TAGS_FILE) as f:
        all_tags = json.load(f)
    tags = []
    for t in all_tags:
        added = t.get('fix_version_added', 'FIX 2.7')
        a_idx = _VERSION_ORDER.index(added) if added in _VERSION_ORDER else 0
        if a_idx <= v_idx:
            t['category'] = _tag_category(t)
            tags.append(t)
    tags.sort(key=lambda t: t['tag'])
    return render_template(
        'fix_reference.html',
        version=version,
        ver_info=ver_info,
        tags_json=json.dumps(tags),
        tag_count=len(tags),
        **_ctx(),
    )



@app.route('/resources')
def resources():
    return render_template('resources.html', **_ctx(preview=request.args.get('preview')))


@app.route('/about')
def about():
    return redirect('/')


@app.route('/tag/<int:tag_number>')
def tag_reference(tag_number):
    try:
        with open(_TAGS_FILE) as f:
            tags = {t['tag']: t for t in json.load(f)}
    except Exception:
        tags = {}
    tag = tags.get(tag_number)
    preview = request.args.get('preview')
    ver = request.args.get('ver', 'fix42')
    if not tag:
        return render_template('stub.html', **_ctx(preview=preview,
            page_title=f'Tag {tag_number} — Not Found',
            page_description=(
                f'Tag {tag_number} is not in our reference yet. '
                'We currently document the 50 most common FIX tags. '
                'More tags are being added regularly.'
            ),
        )), 404
    return render_template('tag_reference.html', **_ctx(preview=preview), tag=tag, ver=ver)


@app.route('/fix-specs')
def fix_specs_redirect():
    return redirect('/message-library')


@app.route('/learn/fix-protocol-101')
def learn_fix_protocol_101():
    return stub('FIX Protocol 101', 'A ground-up introduction to the FIX Protocol — message structure, field types, and the core concepts behind every FIX session.', 'learn')


@app.route('/learn/message-types-guide')
def learn_message_types_guide():
    return stub('Message Types Guide', 'Every FIX message type explained — from New Order Single to Execution Report — with required fields, valid values, and real-world context.', 'learn')


@app.route('/learn/session-management')
def learn_session_management():
    return stub('Session Management', 'How FIX sessions connect, authenticate, and recover — Logon, Heartbeat, ResendRequest, and the full sequence-number lifecycle.', 'learn')


@app.route('/learn/fix-glossary')
def learn_fix_glossary():
    return stub('FIX Glossary', 'Plain-English definitions for every FIX term — from BeginString to execType — with cross-references to relevant tags and message types.', 'learn')




@app.route('/tools/message-builder')
def tools_message_builder():
    with open(_TAGS_FILE) as f:
        tag_list = json.load(f)
    return render_template('message_builder.html',
                           tag_list_json=json.dumps(tag_list),
                           **_ctx(preview=request.args.get('preview')))


@app.route('/tools/tag-validator')
def tools_tag_validator():
    with open(_TAGS_FILE) as f:
        tag_list = json.load(f)
    return render_template('tag_validator.html',
                           tag_list_json=json.dumps(tag_list),
                           **_ctx(preview=request.args.get('preview')))


@app.route('/tools/cert-scripts')
def tools_cert_scripts():
    return stub('Cert Scripts', 'Certification test scripts for FIX connectivity — order entry, drop copy, and allocation flows ready for exchange cert sessions.', 'cert-scripts')

@app.route('/cert/order-entry')
@app.route('/tools/order-entry')
def cert_order_entry():
    return render_template('cert_order_entry.html', **_ctx())


@app.route('/tools/drop-copy')
def tools_drop_copy():
    return stub('Drop Copy', 'Monitor execution reports and order state via drop copy — subscribe to a session and watch fills arrive in real time.', 'tools')


@app.route('/tools/allocation')
def tools_allocation():
    return stub('Allocation', 'Post-trade allocation scripts for FIX — split fills across accounts, generate AllocationInstruction messages, and confirm allocations.', 'tools')


@app.route('/field-reference')
@app.route('/reference')
def field_reference_redirect():
    return redirect('/message-library')


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


@app.route('/troubleshooting/network')
def ts_network():
    return render_template('stub.html', **_ctx(page_title='Network & Connectivity', page_description='Diagnosing FIX network and connectivity issues.', active_nav='troubleshooting'))


@app.route('/troubleshooting/sequence-numbers')
def ts_sequence():
    return render_template('stub.html', **_ctx(page_title='Sequence Number Issues', page_description='Diagnosing and resolving FIX sequence number problems.', active_nav='troubleshooting'))


@app.route('/troubleshooting/logon')
def ts_logon():
    return render_template('stub.html', **_ctx(page_title='Logon Failures', page_description='Diagnosing FIX logon failures and session rejection.', active_nav='troubleshooting'))


@app.route('/troubleshooting/fill-reconciliation')
def ts_fills():
    return render_template('stub.html', **_ctx(page_title='Fill Reconciliation', page_description='Reconciling FIX fills and identifying gaps in execution reports.', active_nav='troubleshooting'))


@app.route('/troubleshooting/rejects')
def ts_rejects():
    return render_template('stub.html', **_ctx(page_title='Order Rejects', page_description='Understanding and resolving FIX order rejects.', active_nav='troubleshooting'))


@app.route('/troubleshooting/latency')
def ts_latency():
    return render_template('stub.html', **_ctx(page_title='Latency & Timing', page_description='Diagnosing FIX message latency and timing issues.', active_nav='troubleshooting'))


@app.route('/troubleshooting/duplicate-orders')
def ts_duplicates():
    return render_template('stub.html', **_ctx(page_title='Duplicate Orders', page_description='Identifying and preventing duplicate FIX orders.', active_nav='troubleshooting'))


@app.route('/troubleshooting/gap-fill')
def ts_gapfill():
    return render_template('stub.html', **_ctx(page_title='Gap Fill & Resend', page_description='Understanding FIX gap fill and resend request procedures.', active_nav='troubleshooting'))


if __name__ == '__main__':
    app.run(debug=True)
