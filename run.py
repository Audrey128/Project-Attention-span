#!/usr/bin/env python3
"""Attention Tracker launcher.

Downloads MediaPipe (first run only), starts a localhost server,
and opens the app in your browser. Standard library only.
"""

import http.server
import os
import socketserver
import sys
import threading
import urllib.request
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8000"))
MP_VERSION = "0.10.14"
CDN = f"https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@{MP_VERSION}"

ASSETS = {
    "vendor/vision_bundle.mjs": f"{CDN}/vision_bundle.mjs",
    "vendor/wasm/vision_wasm_internal.js": f"{CDN}/wasm/vision_wasm_internal.js",
    "vendor/wasm/vision_wasm_internal.wasm": f"{CDN}/wasm/vision_wasm_internal.wasm",
    "vendor/wasm/vision_wasm_nosimd_internal.js": f"{CDN}/wasm/vision_wasm_nosimd_internal.js",
    "vendor/wasm/vision_wasm_nosimd_internal.wasm": f"{CDN}/wasm/vision_wasm_nosimd_internal.wasm",
    "models/face_landmarker.task": (
        "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
        "face_landmarker/float16/1/face_landmarker.task"
    ),
}


def fetch_assets():
    missing = [p for p in ASSETS if not os.path.exists(os.path.join(ROOT, p))]
    if not missing:
        return
    print("First launch: downloading MediaPipe (about 10 MB)...")
    for rel in missing:
        dest = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        tmp = dest + ".part"
        print(f"  {rel}")
        try:
            with urllib.request.urlopen(ASSETS[rel], timeout=60) as r, open(tmp, "wb") as f:
                while chunk := r.read(1 << 16):
                    f.write(chunk)
            os.replace(tmp, dest)
        except Exception as e:
            if os.path.exists(tmp):
                os.remove(tmp)
            sys.exit(f"\nDownload failed for {rel}: {e}\nCheck your internet connection and try again.")
    print("Done. Future launches work offline.\n")


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".wasm": "application/wasm",
        ".task": "application/octet-stream",
    }

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, *a):
        pass


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main():
    fetch_assets()
    try:
        httpd = Server(("127.0.0.1", PORT), Handler)
    except OSError:
        sys.exit(f"Port {PORT} is busy. Close the other app or run: PORT=8001 python3 run.py")
    url = f"http://localhost:{PORT}"
    print(f"Attention Tracker running at {url}  (Ctrl+C to stop)")
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
