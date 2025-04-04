import socket
import threading
import sqlite3
from encryption import encrypt_message, decrypt_message, load_keys
import database  # Ensure the database module is correctly implemented

# Check if authentication module exists
try:
    from authentication import authenticate_user  # Ensure authentication is properly imported
except ModuleNotFoundError:
    print("Warning: 'authentication' module not found. Using a dummy authentication function.")

    def authenticate_user(username, password):
        return True  # Dummy function for testing

# Server Configuration
HOST = "0.0.0.0"
PORT = 5000

# Load RSA keys
try:
    public_key, private_key = load_keys()
except Exception as e:
    print(f"Error loading keys: {e}")
    exit(1)  # Exit if keys can't be loaded

# Store connected clients
clients = {}  # {username: (socket, public_key)}

# Function to handle client messages
def handle_client(client_socket, username):
    try:
        while True:
            encrypted_message = client_socket.recv(4096)
            if not encrypted_message:
                break

            # Decrypt the message
            try:
                message = decrypt_message(encrypted_message, private_key)
                sender, receiver, text = message.split("|", 2)
            except Exception as e:
                print(f"Decryption error: {e}")
                continue

            # Save message to database
            try:
                database.save_message(sender, receiver, text)
            except AttributeError:
                print("Error: 'save_message' function not found in 'database' module.")

            # Forward message if receiver is online
            if receiver in clients:
                receiver_socket, receiver_pub_key = clients[receiver]
                encrypted_response = encrypt_message(f"{sender}|{receiver}|{text}", receiver_pub_key)
                receiver_socket.send(encrypted_response)

    except Exception as e:
        print(f"Error handling client {username}: {e}")
    
    finally:
        # Remove user when they disconnect
        if username in clients:
            del clients[username]
        client_socket.close()
        print(f"{username} disconnected.")

# Function to handle new connections
def handle_new_connection(client_socket):
    try:
        data = client_socket.recv(1024).decode()
        username, password, client_pub_key = data.split("|")

        # Authenticate user
        if authenticate_user(username, password):
            clients[username] = (client_socket, client_pub_key.encode())  # Convert public key to bytes
            client_socket.send("LOGIN_SUCCESS".encode())
            print(f"{username} connected.")

            # Start thread for receiving messages
            threading.Thread(target=handle_client, args=(client_socket, username), daemon=True).start()
        else:
            client_socket.send("LOGIN_FAILED".encode())
            client_socket.close()
    except Exception as e:
        print(f"Error during authentication: {e}")
        client_socket.close()

# Start Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server running on {HOST}:{PORT}")

try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f"New connection from {addr}")
        threading.Thread(target=handle_new_connection, args=(client_socket,), daemon=True).start()
except KeyboardInterrupt:
    print("Shutting down server.")
finally:
    server_socket.close()
