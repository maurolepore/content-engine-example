"""Local dashboard for run outputs. Displays only — never triggers the pipeline.

`python3 -m src.dashboard` serves http://localhost:8080/ and
/api/latest (newest output/run-*.json). Refresh re-reads /output on every call.
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT / "dashboard"
OUTPUT_DIR = ROOT / "output"
PORT = 8080

MIME = {".html": "text/html", ".css": "text/css", ".js": "text/javascript"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/latest":
            return self._send_latest()
        if self.path == "/":
            return self._serve("index.html")
        rel = self.path.lstrip("/")
        if rel in ("style.css", "app.js"):
            return self._serve(rel)
        self.send_error(404)

    def _serve(self, name):
        file = STATIC_DIR / name
        if not file.exists():
            self.send_error(404)
            return
        content = file.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", MIME.get(file.suffix, "text/plain"))
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_latest(self):
        files = sorted(OUTPUT_DIR.glob("run-*.json"))
        if not files:
            self._json({"error": "no runs in /output yet"}, 404)
            return
        latest = files[-1]
        self._json({"file": latest.name, **json.loads(latest.read_text())})

    def _json(self, payload, code=200):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def main():
    print(f"Dashboard → http://localhost:{PORT}")
    print("Displays the latest /output run; pipeline runs from `src.run` only.")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
