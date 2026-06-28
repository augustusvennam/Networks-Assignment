#IMPORTS
import socket

#CONNECTION
HOST = "localhost"
PORT = 5000


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")
    print("Type a request, e.g. CONVERT TEMP C F 25")
    print("Type EXIT or QUIT to close the connection.\n")

    while True:
        request = input("Enter request: ").strip()

        if request.upper() in ("EXIT", "QUIT"):
            break

        if request == "":
            continue

        client_socket.sendall((request + "\n").encode())

        response = client_socket.recv(1024).decode().strip()
        print("Server response:", response, "\n")

    client_socket.close()
    print("Connection closed.")


if __name__ == "__main__":
    main()