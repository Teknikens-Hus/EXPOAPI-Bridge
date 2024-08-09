import http.server
import socketserver
import logging

# Config logging
logging.basicConfig(level=logging.INFO)

logging.log(logging.INFO, "Python webserver script started")

PORT = 8080
FILE_TO_SERVE = 'processed_data.json'
file_path = '/home/app/expoapi-bridge/processed_data.json'

class SingleFileHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/processed_data.json':
            self.path = '/' + FILE_TO_SERVE
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def end_headers(self):
        # Set headers to prevent caching since the file is constantly updated
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')¨
        # Set CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        return super().end_headers()

Handler = SingleFileHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    logging.log(logging.INFO, "Serving file {} on port {}".format(FILE_TO_SERVE, PORT))
    httpd.serve_forever()