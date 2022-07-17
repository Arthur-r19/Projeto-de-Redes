import threading
import socket

PORT = 5050
SERVER = "localhost" # socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
# HEADER = 64
DISCONNECT_MESSAGE = "!CLOSE"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPV4 Adresses with TCP protocol
    client.connect(ADDRESS)
    return client

def send(client, msg):
    client.sendall(msg.encode(FORMAT))

def listen_messages(conn):
    while True:
        msg = conn.recv(1024).decode(FORMAT)
        print(f"\033[999D\033[2K{msg}\033[0m")


def start():
    answer = input('Connect to server? (y/n): ')
    if answer.lower() != 'y':
        return
    name = input('Qual o seu nome? ').capitalize()
    conn = connect()
    thread = threading.Thread(target=listen_messages, args=(conn,), daemon=True)
    thread.start()
    try:
        send(conn, name)
        while True:
            msg = input()
            print('\033[1A\033[999D\033[2K', end='')
            if msg == DISCONNECT_MESSAGE:
                break
            
            send(conn, msg)
        
        send(conn, DISCONNECT_MESSAGE)
    finally:
            pass

start()