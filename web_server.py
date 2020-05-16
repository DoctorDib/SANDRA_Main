import http.server
import socketserver

import config

def start():
    PORT = config.CONFIG["web_server"]["port"]
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()