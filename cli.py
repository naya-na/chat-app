# cclient.py
import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 12350))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                print(message)
        except:
            print("Connection closed.")
            break

def send_messages():
    while True:
        try:
            msg = input()
            client.send(msg.encode())
        except:
            break

# Login interaction
def login():
    for _ in range(2):
        message = client.recv(1024).decode()
        print(message, end='')
        client.send(input().encode())
    print(client.recv(1024).decode())

# Run login and then start chat
login()

threading.Thread(target=receive_messages).start()
threading.Thread(target=send_messages).start()
