#!/usr/bin/env python3
"""Static file server for the dashboard.

Identical to `python3 -m http.server` except it touches data/.active
whenever a data/*.json file is served, so poll.sh can detect browser activity.
"""
import http.server
import os
import pathlib

PORT = 666
ROOT = pathlib.Path(__file__).parent
ACTIVE = ROOT / "data" / ".active"


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/data/") and self.path.endswith(".json"):
            try:
                ACTIVE.touch()
            except OSError:
                pass
        super().do_GET()

    def log_message(self, fmt, *args):
        pass  # suppress per-request noise; errors still go to stderr


if __name__ == "__main__":
    os.chdir(ROOT)
    with http.server.HTTPServer(("", PORT), Handler) as srv:
        print(f"dashboard server listening on :{PORT}", flush=True)
        srv.serve_forever()
