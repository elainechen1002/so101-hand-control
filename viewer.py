"""Serve only the viewer directory on this computer. Ctrl+C stops it."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent / "viewer"
    if not (directory / "node_modules/urdf-loader/src/URDFLoader.js").is_file():
        parser.exit(1, "First run: npm --prefix viewer ci\n")
    handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    except OSError as error:
        parser.exit(1, f"Cannot start viewer: {error}. Try --port 8001\n")
    print(f"SO-101 viewer: http://127.0.0.1:{server.server_port} — Ctrl+C to stop", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
