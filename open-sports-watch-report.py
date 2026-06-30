#!/usr/bin/env python3
"""Serve and open the sports watch comparison report in the default browser."""

from __future__ import annotations

import http.server
import socketserver
import threading
import webbrowser
from pathlib import Path

PORT = 8765
ROOT = Path(__file__).resolve().parent
REPORT = "sports-watch-comparison-report.html"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    report_path = ROOT / REPORT
    if not report_path.is_file():
        raise SystemExit(f"Report not found: {report_path}")

    url = f"http://127.0.0.1:{PORT}/{REPORT}"
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        threading.Timer(0.3, lambda: webbrowser.open(url)).start()
        print(f"Report: {url}")
        print("Press Ctrl+C to stop the local server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
