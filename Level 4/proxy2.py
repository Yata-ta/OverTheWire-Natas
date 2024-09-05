from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import base64

# Define the address and port for the proxy server
PROXY_ADDRESS = '127.0.0.1'
PROXY_PORT = 8081

# Define the credentials for basic authentication
USERNAME = 'natas4'
PASSWORD = 'QryZXc2e0zahULdHrtHxzyYkj59kUxLQ'

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Modify the request headers as needed
        self.headers['Referer'] = 'http://natas5.natas.labs.overthewire.org/'

        # Add basic authentication header
        auth_header = 'Basic ' + base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
        self.headers['Authorization'] = auth_header

        # Forward the request to the target server
        url = self.path
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req) as response:
            # Send the response back to the client
            self.send_response(response.status)
            for header, value in response.headers.items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.read())

def run_proxy_server():
    server_address = (PROXY_ADDRESS, PROXY_PORT)
    httpd = HTTPServer(server_address, ProxyHandler)
    print(f"Proxy server is running at {PROXY_ADDRESS}:{PROXY_PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_proxy_server()
