"""Minimal API and model-service simulator for Kubernetes probes."""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.error import URLError
from urllib.request import urlopen

ROLE = os.environ.get('ROLE', 'model')
MODEL_URL = os.environ.get('MODEL_URL', 'http://127.0.0.1:8081')

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/ready':
            self.send_error(404)
            return
        ready = True
        if ROLE == 'model':
            ready = os.environ.get('MODEL_READY', 'true') == 'true'
        else:
            try:
                with urlopen(MODEL_URL + '/ready', timeout=2) as response:
                    ready = response.status == 200
            except (URLError, OSError):
                ready = False
        self.send_response(200 if ready else 503)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'role': ROLE, 'ready': ready}).encode())

if __name__ == '__main__':
    HTTPServer(('0.0.0.0', int(os.getenv('PORT', '8080'))), Handler).serve_forever()
