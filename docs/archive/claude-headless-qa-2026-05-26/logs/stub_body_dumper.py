from flask import Flask, request, Response, jsonify
import json, datetime, os, gzip

LOG = '/tmp/stub-bodies.log'

app = Flask(__name__)

def log(msg):
    with open('/tmp/stub-server.log', 'a') as f:
        f.write(f'{datetime.datetime.utcnow().isoformat()}Z {msg}\n')

@app.route('/v1/messages', methods=['POST'])
def messages():
    body = request.get_json(silent=True) or {}
    with open(LOG, 'a') as f:
        f.write('=== ' + datetime.datetime.utcnow().isoformat() + ' ===\n')
        f.write(json.dumps(body, indent=2, default=str) + '\n')
    log(f'BODY model={body.get("model")} stream={body.get("stream")} sysprompt_len={len(str(body.get("system", "")))}')
    if body.get('stream'):
        def gen():
            evts = [
                ('message_start', {'type': 'message_start', 'message': {'id': 'msg_x', 'type': 'message', 'role': 'assistant', 'model': body.get('model'), 'content': [], 'stop_reason': None, 'usage': {'input_tokens': 5, 'output_tokens': 0}}}),
                ('content_block_start', {'type': 'content_block_start', 'index': 0, 'content_block': {'type': 'text', 'text': ''}}),
                ('content_block_delta', {'type': 'content_block_delta', 'index': 0, 'delta': {'type': 'text_delta', 'text': 'OK stub.'}}),
                ('content_block_stop', {'type': 'content_block_stop', 'index': 0}),
                ('message_delta', {'type': 'message_delta', 'delta': {'stop_reason': 'end_turn'}, 'usage': {'output_tokens': 2}}),
                ('message_stop', {'type': 'message_stop'}),
            ]
            for evt, data in evts:
                yield f'event: {evt}\ndata: {json.dumps(data)}\n\n'
        return Response(gen(), mimetype='text/event-stream')
    return jsonify({'id': 'msg_x', 'type': 'message', 'role': 'assistant', 'model': body.get('model'), 'content': [{'type': 'text', 'text': 'OK stub.'}], 'stop_reason': 'end_turn', 'usage': {'input_tokens': 5, 'output_tokens': 2}})

if __name__ == '__main__':
    open(LOG, 'w').close()
    app.run(host='127.0.0.1', port=8089, debug=False)
