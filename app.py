from flask import Flask, render_template, request, jsonify
from fix_decoder import decode_fix, generate_summary

app = Flask(__name__)


def stub(title, description, active_nav=''):
    return render_template('stub.html',
                           page_title=title,
                           page_description=description,
                           active_nav=active_nav)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/decode', methods=['POST'])
def decode():
    raw = request.form.get('fix_message', '').strip()
    fields, status = decode_fix(raw)
    if status == 'ok' and fields:
        summary = generate_summary(fields)
        return jsonify({'status': 'ok', 'fields': fields, 'summary': summary})
    return jsonify({'status': status})


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
