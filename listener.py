import socket
import sys

def send_request(method, encoding, data, uri, filename, host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        request_data = f"{method}|{encoding}|{data}|{uri}|{filename}"
        print(f"[+] Sending data to server: {request_data}")

        client_socket.send(request_data.encode())

        received_data = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            received_data += chunk

        if received_data.startswith(b"Error"):
            print("[!] Error: Server could not generate CSRF PoC.")
        else:
            with open(filename, "wb") as f:
                f.write(received_data)
            print(f"[+] CSRF PoC HTML file received and saved as {filename}")

        client_socket.close()
    
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv)!= 6:
        print("Usage: python listener.py <method> <encoding> <data> <uri> <filename>")
        sys.exit(1)

    method = sys.argv[1]
    encoding = sys.argv[2]
    data = sys.argv[3]
    uri = sys.argv[4]
    filename = sys.argv[5]

    send_request(method, encoding, data, uri, filename, "127.0.0.1", 4444)
