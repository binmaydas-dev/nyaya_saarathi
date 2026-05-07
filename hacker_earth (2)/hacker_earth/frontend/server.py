from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_ORIGIN = "http://127.0.0.1:8000"
ROOT = Path(__file__).resolve().parent


class NyayaMitraHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if path == "/":
            path = "/index.html"
        clean_path = path.split("?", 1)[0].lstrip("/")
        return str(ROOT / clean_path)

    def do_GET(self):
        if self.path.startswith("/api/"):
            self.proxy_request()
            return
        super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            self.proxy_request()
            return
        self.send_error(404, "Not found")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def proxy_request(self):
        target_path = self.path[4:] if self.path.startswith("/api") else self.path
        target_url = f"{API_ORIGIN}{target_path}"
        body = None
        headers = {}

        if self.command in {"POST", "PUT", "PATCH"}:
            if "chunked" in self.headers.get("Transfer-Encoding", "").lower():
                body_parts = []
                while True:
                    line = self.rfile.readline().strip()
                    try:
                        chunk_size = int(line, 16)
                    except ValueError:
                        break
                    if chunk_size == 0:
                        self.rfile.readline()
                        break
                    body_parts.append(self.rfile.read(chunk_size))
                    self.rfile.readline()
                body = b"".join(body_parts)
            else:
                length = int(self.headers.get("Content-Length", "0") or "0")
                body = self.rfile.read(length) if length > 0 else None
            content_type = self.headers.get("Content-Type")
            if content_type:
                headers["Content-Type"] = content_type

        request = Request(target_url, data=body, method=self.command, headers=headers)

        try:
            with urlopen(request, timeout=30) as response:
                payload = response.read()
                self.send_response(response.status)
                self.send_cors_headers()
                self.send_header("Content-Type", response.headers.get("Content-Type", "application/json"))
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
        except HTTPError as error:
            payload = error.read()
            self.send_response(error.code)
            self.send_cors_headers()
            self.send_header("Content-Type", error.headers.get("Content-Type", "application/json"))
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        except URLError as error:
            payload = f'{{"status":"error","message":"Backend unavailable: {error.reason}"}}'.encode()
            self.send_response(502)
            self.send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 5173), NyayaMitraHandler)
    print("NyayaMitra frontend running at http://127.0.0.1:5173")
    server.serve_forever()
