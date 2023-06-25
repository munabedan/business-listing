
import http.server
import socketserver
import os

PORT = 5000

web_dir = os.path.join(os.path.dirname(__file__), 'site')
os.chdir(web_dir)

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print(f"Serving HTML files at http://localhost:{PORT}")
httpd.serve_forever()
