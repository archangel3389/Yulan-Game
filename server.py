import time, math, random, os, socket, sys, threading, json, requests
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Text
from tkinter import Frame
from tkinter import Canvas
from tkinter import Scrollbar
from tkinter import Listbox
from tkinter import LabelFrame
from tkinter import Radiobutton
from tkinter import Checkbutton
from tkinter import OptionMenu
from tkinter import Scale

window = tk.Tk()
window.title("Server")
window.geometry("500x600")

def start_server():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with open('server.conf', 'r') as config_file:
        lines = config_file.readlines()
        serverIP = socket.gethostbyname(socket.gethostname())
        serverPort = 6666
        for line in lines:
            if line.startswith('serverIP='):
                serverIP = line.split('=')[1].strip()
            elif line.startswith('serverPort='):
                serverPort = int(line.split('=')[1].strip())
    server.bind((serverIP, serverPort))
    server.listen(5)
    threading.Thread(target=accept_connections, daemon=True).start()

def accept_connections():
    log_text.insert(tk.INSERT, f"Server started on {server.getsockname()[0]}:{server.getsockname()[1]}\n")
    while True:
        client, clientaddress = server.accept()
        log_text.insert(tk.INSERT, f"Connection from {clientaddress} has been established!\n")
        client_thread = threading.Thread(target=handle_client, args=(client, clientaddress), daemon=True, name=str(clientaddress[0]))
        client_thread.start()

def handle_client(client, clientaddress):
    client.send("Welcome to the server!".encode())
    
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            log_text.insert(tk.INSERT, f"Received data from {clientaddress}: {data.decode()}\n")
            client.send(data)
            
            # Place your game logic here
            # Example:
            # game_data = process_game_logic(data)
            # client.send(game_data)
            
        except ConnectionResetError:
            break
    log_text.insert(tk.INSERT, f"Connection from {clientaddress} has been closed\n")
    client.close()

def stop_server():
    server.close()
    log_text.insert(tk.INSERT, "Server stopped\n")


def open_connection_settings():
    settings_window = tk.Toplevel(window)
    settings_window.title("Connection Settings")
    settings_window.geometry("300x200")

    Label(settings_window, text="IP Address:").pack()
    ip_entry = Entry(settings_window)
    ip_entry.pack()

    Label(settings_window, text="Port:").pack()
    port_entry = Entry(settings_window)
    port_entry.pack()

    def save_settings():
        ip = ip_entry.get()
        port = port_entry.get()
        with open('server.conf', 'w') as config_file:
            config_file.write(f"serverIP={ip}\nserverPort={port}\n")
        log_text.insert(tk.INSERT, f"Connection settings saved\n")

        settings_window.destroy()

    save_button = Button(settings_window, text="Save", command=save_settings)
    save_button.pack()

log_text = scrolledtext.ScrolledText(window, width=80, height=25)
log_text.pack()

button_frame = Frame(window)
button_frame.pack()

start_button = Button(button_frame, text="Start Server", command=start_server)
start_button.grid(row=0, column=0, padx=5, pady=5)

stop_button = Button(button_frame, text="Stop Server", command=stop_server)
stop_button.grid(row=0, column=1, padx=5, pady=5)

settings_button = Button(button_frame, text="Connection Settings", command=open_connection_settings)
settings_button.grid(row=0, column=2, padx=5, pady=5)

def kickPlayerMenue():
    kick_window = tk.Toplevel(window)
    kick_window.title("Kick Player")
    kick_window.geometry("300x200")

    Label(kick_window, text="Player IP Address:").pack()
    ip_entry = Entry(kick_window)
    ip_entry.pack()

    def kick_player():
        ip = ip_entry.get()
        for thread in threading.enumerate():
            if thread.name == ip:
                thread._stop()
            break
        log_text.insert(tk.INSERT, f"Player with IP {ip} has been kicked\n")
        kick_window.destroy()

    kick_button = Button(kick_window, text="Kick", command=kick_player)
    kick_button.pack()

kick_button = Button(button_frame, text="Kick Player", command=kickPlayerMenue)
kick_button.grid(row=1, column=0, padx=5, pady=5)

placeholder2 = Button(button_frame, text="Placeholder 2")
placeholder2.grid(row=1, column=1, padx=5, pady=5)

placeholder3 = Button(button_frame, text="Placeholder 3")
placeholder3.grid(row=1, column=2, padx=5, pady=5)

window.mainloop()
