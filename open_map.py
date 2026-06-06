import webbrowser
from http.server import SimpleHTTPRequestHandler
import socketserver
import os, threading
from http.server import HTTPServer

PORT = 8000

os.chdir(os.path.dirname(__file__))

threading.Thread(
    target=lambda: HTTPServer(("localhost", PORT), SimpleHTTPRequestHandler).serve_forever(),
    daemon=True
).start()

webbrowser.open(f"http://localhost:{PORT}/map.html")

input("Enter to exit...\n")


