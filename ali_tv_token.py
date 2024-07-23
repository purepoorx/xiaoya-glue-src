#!/usr/local/bin/python3

import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        if 'refresh_token' in data:
            refresh_token = data['refresh_token']
            token_info = requests.post('http://api.extscreen.com/aliyundrive/token', data={'refresh_token': refresh_token,}).json()['data']
            del token_info['code']
            del token_info['message']
            new_token_info = str(token_info).replace("'", '"')
            token_info=new_token_info.replace(" ", '')
            print(token_info)
        else:
            print("'refresh_token' not found in the request.")
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(token_info.encode(encoding='utf_8'))

if __name__ == '__main__':
    # Create the server
    server = HTTPServer(('0.0.0.0', 80), RequestHandler)
    print("Ali Auth Server listening on http://0.0.0.0:80")
    
    # Start the server
    server.serve_forever()
