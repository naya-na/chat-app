import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("localhost", 12350))
        self.username = ""
        self.window = tk.Tk()
        self.window.withdraw()
        self.login_screen()

    def login_screen(self):
        login_win = tk.Toplevel()
        login_win.title("Login")

        tk.Label(login_win, text="Username:").pack()
        username_entry = tk.Entry(login_win)
        username_entry.pack()

        tk.Label(login_win, text="Password:").pack()
        password_entry = tk.Entry(login_win, show="*")
        password_entry.pack()

        def try_login():
            self.client.recv(1024)  # Username prompt
            self.client.send(username_entry.get().encode())

            self.client.recv(1024)  # Password prompt
            self.client.send(password_entry.get().encode())

            response = self.client.recv(1024).decode()
            if "successful" in response:
                self.username = username_entry.get()
                messagebox.showinfo("Login", "Login Successful!")
                login_win.destroy()
                self.chat_window()
            else:
                messagebox.showerror("Login Failed", response)

        tk.Button(login_win, text="Login", command=try_login).pack()

    def chat_window(self):
        self.window.deiconify()
        self.window.title(f"Chat - {self.username}")
        self.window.geometry("400x500")

        self.chat_area = scrolledtext.ScrolledText(self.window, state='disabled')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.msg_entry = tk.Entry(self.window)
        self.msg_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.msg_entry.bind("<Return>", lambda event: self.send_msg())

        send_btn = tk.Button(self.window, text="Send", command=self.send_msg)
        send_btn.pack(pady=(0, 10))

        # Start receiving messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.window.protocol("WM_DELETE_WINDOW", self.close_connection)
        self.window.mainloop()

    def send_msg(self):
        msg = self.msg_entry.get()
        if msg:
            self.client.send(msg.encode())
            self.msg_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                msg = self.client.recv(1024).decode()
                if msg:
                    self.chat_area.config(state='normal')
                    self.chat_area.insert(tk.END, msg + "\n")
                    self.chat_area.yview(tk.END)
                    self.chat_area.config(state='disabled')
            except:
                break

    def close_connection(self):
        self.client.close()
        self.window.destroy()

# Run the GUI client
if __name__ == "__main__":
    ChatClient()
