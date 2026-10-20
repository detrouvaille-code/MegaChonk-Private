"""Serve this checkout locally, then open the game once the port is bound."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import socket
from urllib.request import urlopen
from urllib.parse import urlencode
import webbrowser


ROOT = Path(__file__).resolve().parent.parent


class LocalGameHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Artist revisions should appear on reload during local development.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


class LocalGameServer(ThreadingHTTPServer):
    allow_reuse_address = False

    def server_bind(self):
        # Windows otherwise permits two Python HTTP servers on the same port.
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        super().server_bind()


def checkout_is_served():
    try:
        for name in ("index.html", "game.js"):
            with urlopen(f"http://127.0.0.1:4173/{name}?v=tactical-fur-20261019", timeout=3) as response:
                if response.read() != (ROOT / name).read_bytes():
                    return False
        return True
    except OSError:
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--character", choices=("van", "tactical-tabby"))
    args = parser.parse_args()
    query = {"v": "tactical-fur-20261019"}
    if args.character:
        query["character"] = args.character
    url = "http://127.0.0.1:4173/?" + urlencode(query)
    handler = partial(LocalGameHandler, directory=str(ROOT))
    try:
        server = LocalGameServer(("127.0.0.1", 4173), handler)
    except OSError as error:
        if checkout_is_served():
            print(f"This Mega Chonk checkout is already running: {url}", flush=True)
            if not args.no_browser:
                webbrowser.open(url)
            return
        parser.exit(1, f"Could not start Mega Chonk on port 4173: {error}\nClose the other local server, then try again.\n")
    with server:
        print(f"Mega Chonk: {url}\nKeep this window open while playing. Ctrl+C stops the server.", flush=True)
        if not args.no_browser:
            webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
