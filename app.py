from flask import Flask, render_template, request, jsonify
from fix_decoder import decode_fix, generate_summary

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)
