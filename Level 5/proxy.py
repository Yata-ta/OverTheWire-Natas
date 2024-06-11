from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import base64
import requests

# Define the address and port for the proxy server
PROXY_ADDRESS = '127.0.0.1'
PROXY_PORT = 8080

# Define the credentials for basic authentication
USERNAME = 'natas5'
PASSWORD = 'Z0NsrtIkJoKALBCLi5eqFfcRN82Au2oD'

MODIFY = True
REFERER = ""
COOKIES = ["loggedin=1"]

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        if (MODIFY == True and REFERER != ""):
            # Modify the request headers as needed
            self.headers['Referer'] = REFERER

        # Add basic authentication header
        auth_header = 'Basic ' + base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
        self.headers['Authorization'] = auth_header

        if (MODIFY == True and COOKIES != ""):

            self.headers['Cookie'] = ";".join(COOKIES)
            
        print(self.headers)


        # Forward the request to the target server
        url = self.path
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req) as response:
        
            payload_received = response.read()
            print("Payload Received:\n{}".format(payload_received.decode()))


            

            # Check if there are any cookies in the response
            if 'Set-Cookie' in response.headers:
                print("Cookies:")
                print(response.headers['Set-Cookie'])

            
            # Send the response back to the client
            self.send_response(response.status)
            for header, value in response.headers.items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(payload_received)

def run_proxy_server():
    server_address = (PROXY_ADDRESS, PROXY_PORT)
    httpd = HTTPServer(server_address, ProxyHandler)
    print(f"Proxy server is running at {PROXY_ADDRESS}:{PROXY_PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_proxy_server()
