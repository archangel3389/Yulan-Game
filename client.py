import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

def create_menu(root, set_server_callback):
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    server_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Server", menu=server_menu)
    server_menu.add_command(label="Set Server", command=set_server_callback)

def set_server(root, connect_to_server_callback):
    server_window = tk.Toplevel(root)
    server_window.title("Set Server")

    tk.Label(server_window, text="Server IP:").pack(padx=10, pady=5)
    server_ip_entry = tk.Entry(server_window)
    server_ip_entry.pack(padx=10, pady=5)

    tk.Label(server_window, text="Server Port:").pack(padx=10, pady=5)
    server_port_entry = tk.Entry(server_window)
    server_port_entry.pack(padx=10, pady=5)

    def on_connect():
        server_ip = server_ip_entry.get()
        server_port = int(server_port_entry.get())
        server_window.destroy()
        connect_to_server_callback(server_ip, server_port)

    tk.Button(server_window, text="Connect", command=on_connect).pack(padx=10, pady=10)

def connect_to_server(server_ip, server_port, chat_area, entry_message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    chat_area.config(state='normal')
                    chat_area.insert(tk.END, message + '\n')
                    chat_area.config(state='disabled')
                    chat_area.yview(tk.END)
            except ConnectionAbortedError:
                break
            except Exception as e:
                print(f"Error: {e}")
                break

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.daemon = True
    receive_thread.start()

    def send_message(event=None):
        message = entry_message.get()
        client_socket.sendall(message.encode('utf-8'))
        entry_message.delete(0, tk.END)

    entry_message.bind("<Return>", send_message)

    def refresh_chat_area():
        chat_area.config(state='normal')
        chat_area.insert(tk.END, '')  # This line is just to trigger the refresh
        chat_area.config(state='disabled')
        chat_area.yview(tk.END)
        root.after(2000, refresh_chat_area)  # Schedule the function to be called again after 2 seconds

    refresh_chat_area()  # Start the periodic refresh

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Kulan Client")

    chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
    chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    entry_message = tk.Entry(root)
    entry_message.pack(padx=10, pady=10, fill=tk.X, expand=True)

    create_menu(root, lambda: set_server(root, lambda ip, port: connect_to_server(ip, port, chat_area, entry_message)))

    root.mainloop()
