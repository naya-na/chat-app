import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from encryption import encrypt_message, decrypt_message, load_keys

# Load RSA keys
public_key, private_key = load_keys()

# Client Variables
client_socket = None
username = None

# GUI Initialization
root = tk.Tk()
root.title("ChatApp Login")
root.geometry("400x500")

tk.Label(root, text="Server IP:").pack()
server_ip_entry = tk.Entry(root)
server_ip_entry.pack()

tk.Label(root, text="Port:").pack()
port_entry = tk.Entry(root)
port_entry.pack()

tk.Label(root, text="Username:").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Label(root, text="Recipient:").pack()
recipient_entry = tk.Entry(root)
recipient_entry.pack()

def register():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    
    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty!")
        return

    success = register_user(username, password)
    
    if success:
        messagebox.showinfo("Success", "Registration Successful! You can now log in.")
    else:
        messagebox.showerror("Error", "Username already exists or registration failed.")


# Function to send messages
def send_message():
    message = msg_entry.get()
    recipient = recipient_entry.get()
    
    if message and recipient:
        encrypted_msg = encrypt_message(f"{username}|{recipient}|{message}", public_key)
        client_socket.send(encrypted_msg)
        chat_box.insert(tk.END, f"You → {recipient}: {message}\n", "user_message")
        msg_entry.delete(0, tk.END)

# Function to receive messages
def receive_messages():
    while True:
        try:
            encrypted_message = client_socket.recv(4096)
            if not encrypted_message:
                break
            message = decrypt_message(encrypted_message, private_key)
            sender, _, text = message.split("|", 2)
            chat_box.insert(tk.END, f"{sender}: {text}\n", "received_message")
        except:
            break

# Chat Window
# Chat Window
def open_chat_window():
    global chat_box, msg_entry, recipient_entry  # Ensure recipient_entry is accessible

    chat_window = tk.Tk()
    chat_window.title(f"ChatApp - {username}")
    chat_window.geometry("500x600")

    chat_box = scrolledtext.ScrolledText(chat_window, width=60, height=25)
    chat_box.pack(pady=10)

    # Recipient Entry
    tk.Label(chat_window, text="Recipient Username:").pack()
    recipient_entry = tk.Entry(chat_window, width=40)
    recipient_entry.pack(pady=5)

    # Message Entry
    msg_entry = tk.Entry(chat_window, width=40)
    msg_entry.pack(side=tk.LEFT, padx=10, pady=10)

    send_button = tk.Button(chat_window, text="Send", command=send_message)
    send_button.pack(side=tk.RIGHT, padx=10, pady=10)

    chat_box.tag_config("user_message", foreground="blue")
    chat_box.tag_config("received_message", foreground="green")

    threading.Thread(target=receive_messages, daemon=True).start()
    chat_window.mainloop()

# Function to connect to server
def connect_to_server():
    global client_socket, username

    username = username_entry.get()
    password = password_entry.get()
    SERVER_IP = server_ip_entry.get()
    PORT = int(port_entry.get())

    if not SERVER_IP or not PORT:
        messagebox.showerror("Error", "Enter Server IP and Port!")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORT))
        client_socket.send(f"{username}|{password}|{public_key}".encode())

        response = client_socket.recv(1024).decode()
        if response == "LOGIN_SUCCESS":
            root.destroy()
            open_chat_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            client_socket.close()

    except Exception as e:
        messagebox.showerror("Connection Error", f"Failed to connect: {e}")

# Buttons
login_button = tk.Button(root, text="Login", command=connect_to_server)
login_button.pack(pady=10)

root.mainloop()
