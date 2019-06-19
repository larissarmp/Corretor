#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import re
from pathlib import Path

from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler

import core.runner as runner

ROOT = Path(Path(__file__).resolve().parent / 'GUI')

class StaticServer(BaseHTTPRequestHandler):

    def do_GET(self):
        filePath = ROOT
        if self.path == '/':
            filename = 'index.html'
        else:
            filename = self.path
        filename = re.sub(r'^[\./]', '', filename)
        
        self.send_response(200)
        if filename[-4:] == '.css':
            self.send_header('Content-type', 'text/css')
        elif filename[-5:] == '.json':
            self.send_header('Content-type', 'application/json')
        elif filename[-3:] == '.js':
            self.send_header('Content-type', 'application/javascript')
        elif filename[-4:] == '.ico':
            self.send_header('Content-type', 'image/x-icon')
        else:
            self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        with open(filePath.joinpath(filename), 'rb') as fh:
            html = fh.read()
            #html = bytes(html, 'utf8')
            self.wfile.write(html)
            
    
    def do_POST(self):
        length = int(self.headers['content-length'])
        postvars = parse_qs( self.rfile.read(length), keep_blank_values=1)
        response = runner.run(postvars[b'entrada'][0].decode("utf-8"))
        print(response)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))
        self.wfile.close()
 
def run(server_class=HTTPServer, handler_class=StaticServer, port=8083):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()
 
run()