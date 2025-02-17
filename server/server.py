import http.server
import socketserver
import os

PORT = 8000

# Change the directory to one level up
os.chdir('..')  # Go up one directory from the current directory

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
