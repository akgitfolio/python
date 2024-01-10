from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import os
import mimetypes
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        try:
            file_path = os.path.join(STATIC_DIR, self.path[1:])
            with open(file_path, "rb") as file:
                content = file.read()
                content_type, _ = mimetypes.guess_type(self.path)
                if content_type is None:
                    content_type = "application/octet-stream"
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()
                self.wfile.write(content)
                logger.info("GET request successful: %s", self.path)
        except FileNotFoundError:
            self.send_error(404, "File Not Found: %s" % self.path)
            logger.error("File Not Found: %s", self.path)
        except Exception as e:
            self.send_error(500, "Internal Server Error: %s" % str(e))
            logger.error("Error serving %s: %s", self.path, str(e))

    def do_POST(self):
        try:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = b"POST request received!"
            self.wfile.write(response)
            logger.info("POST request successful")
        except Exception as e:
            self.send_error(500, "Internal Server Error: %s" % str(e))
            logger.error("Error handling POST request: %s", str(e))


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def run(server_class=ThreadedHTTPServer, handler_class=SimpleHTTPRequestHandler):
    print("Starting server...")

    server_address = ("127.0.0.1", 8080)
    httpd = server_class(server_address, handler_class)

    print("Server is running...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server is stopping...")
        httpd.server_close()
        print("Server stopped.")


if __name__ == "__main__":
    run()
