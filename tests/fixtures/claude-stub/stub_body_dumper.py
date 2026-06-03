#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.10"
# dependencies = ["flask>=3.0"]
# ///
"""Body-capturing variant of ``stub.py`` for assertion-driven QA.

Identical wire behavior to ``stub.py`` (Anthropic Messages v1 shape,
both JSON and SSE), but writes the full request body for every
``/v1/messages`` POST to a separate dump log so callers can assert
against ``system[]``, ``messages[]``, headers, etc.

Use this for F9 (output-style content reaching ``system[2]``) and F7
(resolved slash-command body reaching ``messages[]``). For F5 the
sentinel files written by the hook itself are the observable, not the
request body — so plain ``stub.py`` suffices there.

Env vars:

  STUB_PORT       - bind port (default 8089)
  STUB_HOST       - bind host (default 127.0.0.1)
  STUB_LOG        - access-log path (default /tmp/stub-server.log)
  STUB_BODIES_LOG - body-dump path (default /tmp/stub-bodies.log)
"""
from flask import Flask, request, Response, jsonify
import datetime
import json
import os
import signal
import sys

LOG = os.environ.get('STUB_LOG', '/tmp/stub-server.log')
BODIES_LOG = os.environ.get('STUB_BODIES_LOG', '/tmp/stub-bodies.log')
PORT = int(os.environ.get('STUB_PORT', '8089'))
HOST = os.environ.get('STUB_HOST', '127.0.0.1')

app = Flask(__name__)


def log(msg):
    with open(LOG, 'a') as f:
        f.write(f'{datetime.datetime.utcnow().isoformat()}Z {msg}\n')


@app.route('/v1/messages', methods=['POST'])
def messages():
    body = request.get_json(silent=True) or {}
    with open(BODIES_LOG, 'a') as f:
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


@app.route('/v1/messages/count_tokens', methods=['POST'])
def count_tokens():
    return jsonify({'input_tokens': 10})


@app.route('/v1/models', methods=['GET'])
def list_models():
    return jsonify({'data': [
        {'id': 'claude-sonnet-4-5', 'display_name': 'Sonnet Stub', 'type': 'model'},
        {'id': 'claude-opus-4-7', 'display_name': 'Opus Stub', 'type': 'model'}
    ], 'has_more': False, 'first_id': 'claude-sonnet-4-5', 'last_id': 'claude-opus-4-7'})


def _shutdown(signum, _frame):
    log(f'SHUTDOWN signal={signum}')
    sys.exit(0)


if __name__ == '__main__':
    # Fresh logs per run.
    open(LOG, 'w').close()
    open(BODIES_LOG, 'w').close()
    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)
    app.run(host=HOST, port=PORT, debug=False)
