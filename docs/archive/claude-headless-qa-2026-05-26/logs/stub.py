from flask import Flask, request, jsonify, Response
import json, time, sys, datetime, os

LOG = '/tmp/stub-server.log'

def log(msg):
    line = f'{datetime.datetime.utcnow().isoformat()}Z {msg}\n'
    with open(LOG, 'a') as f:
        f.write(line)
    print(line, end='', flush=True)

app = Flask(__name__)

@app.before_request
def trace():
    log(f'REQ {request.method} {request.path} headers={dict(request.headers)}')

@app.route('/v1/messages', methods=['POST'])
def messages():
    body = request.get_json(silent=True) or {}
    log(f'BODY model={body.get("model")} stream={body.get("stream")} msgs={len(body.get("messages", []))}')
    model = body.get('model', 'claude-sonnet-4-5')
    if body.get('stream'):
        # SSE streaming response per Anthropic spec
        def gen():
            msg_id = 'msg_stub_001'
            evts = [
                ('message_start', {'type': 'message_start', 'message': {
                    'id': msg_id, 'type': 'message', 'role': 'assistant',
                    'model': model, 'content': [], 'stop_reason': None,
                    'stop_sequence': None, 'usage': {'input_tokens': 5, 'output_tokens': 0}}}),
                ('content_block_start', {'type': 'content_block_start', 'index': 0,
                    'content_block': {'type': 'text', 'text': ''}}),
                ('content_block_delta', {'type': 'content_block_delta', 'index': 0,
                    'delta': {'type': 'text_delta', 'text': 'OK stub.'}}),
                ('content_block_stop', {'type': 'content_block_stop', 'index': 0}),
                ('message_delta', {'type': 'message_delta',
                    'delta': {'stop_reason': 'end_turn', 'stop_sequence': None},
                    'usage': {'output_tokens': 2}}),
                ('message_stop', {'type': 'message_stop'}),
            ]
            for evt, data in evts:
                yield f'event: {evt}\ndata: {json.dumps(data)}\n\n'
        return Response(gen(), mimetype='text/event-stream')
    return jsonify({
        'id': 'msg_stub_001', 'type': 'message', 'role': 'assistant',
        'model': model, 'content': [{'type': 'text', 'text': 'OK stub.'}],
        'stop_reason': 'end_turn', 'stop_sequence': None,
        'usage': {'input_tokens': 5, 'output_tokens': 2}
    })

@app.route('/v1/messages/count_tokens', methods=['POST'])
def count_tokens():
    return jsonify({'input_tokens': 10})

@app.route('/v1/models', methods=['GET'])
def list_models():
    return jsonify({'data': [
        {'id': 'claude-sonnet-4-5', 'display_name': 'Sonnet Stub', 'type': 'model'},
        {'id': 'claude-opus-4-7', 'display_name': 'Opus Stub', 'type': 'model'}
    ], 'has_more': False, 'first_id': 'claude-sonnet-4-5', 'last_id': 'claude-opus-4-7'})

@app.route('/<path:p>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catchall(p):
    log(f'CATCHALL {request.method} /{p}')
    return jsonify({'error': {'type': 'stub_catchall', 'path': p}}), 404

if __name__ == '__main__':
    open(LOG, 'w').close()
    log('STARTING stub on :8088')
    app.run(host='127.0.0.1', port=8088, debug=False)
