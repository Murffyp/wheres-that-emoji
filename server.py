#!/usr/bin/env python3
"""
Emoji Fuzzy Search Server
Usage: python3 server.py [port]
Defaults: port=7700
"""

import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

def load_emojis(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        groups = json.load(f)
    flat = []
    for group in groups:
        for subgroup in group.get('subgroups', []):
            for emoji in subgroup.get('emojis', []):
                flat.append({
                    'emoji': emoji.get('emoji', ''),
                    'description': emoji.get('description', ''),
                    'code_point': emoji.get('code_point', emoji.get('code_point(s)', '')),
                    'type_field': emoji.get('type_field', ''),
                    'group': group.get('name', ''),
                    'subgroup': subgroup.get('name', ''),
                    'keywords': emoji.get('keywords', [])
                })
    return flat

class Handler(BaseHTTPRequestHandler):
    emojis = []
    base_dir = '.'

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == '/api/emojis':
            data = json.dumps(self.emojis).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(data))
            self.end_headers()
            self.wfile.write(data)

        elif parsed.path == '/' or parsed.path == '/index.html':
            self._serve_file('index.html', 'text/html; charset=utf-8')

        elif parsed.path.startswith('/fonts/'):
            self._serve_file(parsed.path.lstrip('/'), 'font/ttf')

        else:
            self.send_response(404)
            self.end_headers()

    def _serve_file(self, relative_path, content_type):
        full_path = os.path.join(self.base_dir, relative_path)
        if os.path.exists(full_path):
            with open(full_path, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(data))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()
    
if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7700
    json_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), 'emojis.json')

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found!")
        sys.exit(1)

    print(f"Loading emojis from {json_path}...")
    Handler.emojis = load_emojis(json_path)
    Handler.base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Loaded {len(Handler.emojis)} emojis")
    print(f"Starting server on http://localhost:{port}")

    server = HTTPServer(('0.0.0.0', port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
