#!/usr/bin/env python3
"""Serve and open the sports watch comparison report in the default browser."""

from __future__ import annotations

import argparse
import http.server
import socket
import socketserver
import sys
import threading
import webbrowser
from pathlib import Path

DEFAULT_PORT = 8765
ROOT = Path(__file__).resolve().parent
REPORT = "sports-watch-comparison-report.html"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format: str, *args) -> None:
        return


def find_free_port(start: int = DEFAULT_PORT, attempts: int = 10) -> int:
    for port in range(start, start + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if sock.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise RuntimeError(f"No free port found near {start}")


def open_browser(url: str) -> None:
    try:
        opened = webbrowser.open(url)
    except Exception as exc:  # noqa: BLE001 - show any browser launcher failure
        print(f"Could not launch browser automatically: {exc}", file=sys.stderr)
        opened = False
    if not opened:
        print("Browser did not open automatically. Copy this URL into your browser:")
        print(url)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Open the sports watch comparison HTML report in a browser."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Local server port (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Only start the local server; do not try to open a browser window.",
    )
    args = parser.parse_args()

    report_path = ROOT / REPORT
    if not report_path.is_file():
        print("Report file not found.", file=sys.stderr)
        print(f"Expected: {report_path}", file=sys.stderr)
        print("Run this command from the repository root:", file=sys.stderr)
        print("  python3 open-sports-watch-report.py", file=sys.stderr)
        raise SystemExit(1)

    port = args.port
    try:
        httpd = socketserver.TCPServer(("127.0.0.1", port), Handler)
    except OSError:
        port = find_free_port(args.port + 1)
        httpd = socketserver.TCPServer(("127.0.0.1", port), Handler)
        print(f"Port {args.port} is busy, using {port} instead.")

    url = f"http://127.0.0.1:{port}/{REPORT}"
    print("Starting local report server...")
    print(f"Open in browser: {url}")
    print("Stop server with Ctrl+C.")

    if not args.no_browser:
        threading.Timer(0.3, lambda: open_browser(url)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
