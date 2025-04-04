# sserver.py
import socket
import threading

users = {
    "user1": "pass1",
    "user2": "pass2"
}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    conn.send("Username: ".encode())
    username = conn.recv(1024).decode()
    conn.send("Password: ".encode())
    password = conn.recv(1024).decode()

    if username in users and users[username] == password:
        conn.send("Login successful! You can start chatting.\n".encode())
    else:
        conn.send("Login failed! Disconnecting.".encode())
        conn.close()
        return

    # Start thread for receiving messages from client
    threading.Thread(target=receive_messages_from_client, args=(conn, username)).start()

    # Send messages from server manually
    while True:
        try:
            msg = input(f"[Server to {username}]: ")
            if msg.lower() == "exit":
                conn.send("Server has closed the connection.".encode())
                conn.close()
                break
            conn.send(f"Server: {msg}".encode())
        except:
            break

def receive_messages_from_client(conn, username):
    while True:
        try:
            message = conn.recv(1024).decode()
            if not message:
                break
            print(f"[{username}]: {message}")
        except:
            break

# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 12350))
server.listen()

print("[STARTED] Server is listening on port 12350...")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
