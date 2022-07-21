import threading
import socket
import random
from datetime import datetime

PORT = 5050
SERVER = "localhost" # socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
# HEADER = 64
DISCONNECT_MESSAGE = "!CLOSE"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPV4 Adresses with TCP protocol
server.bind(ADDRESS)

clients = set()
clients_lock = threading.Lock() 


def start():
    print('\033[1;41m[SERVER STARTED]\033[0m')
    server.listen()
    while True:
        conn, addr = server.accept()
        with clients_lock: # Prevent multiple threads to modify "clients" simultaneously 
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # handling each client on a separated thread
        thread.start()

def handle_client(conn, addr):
    name = conn.recv(1024).decode(FORMAT)
    color = random.randint(31, 37)
    help_msg = f'\033[1;41m[SERVER]\033[0m Envie \033[1;31m!HELP\033[0m para mais informações'
    wlc_msg = f'\033[1;41m[SERVER]\033[0m \033[1;{color}m{name}\033[0m ENTROU NO CHAT!'
    frwl_msg = f'\033[1;41m[SERVER]\033[0m \033[1;{color}m{name}\033[0m SAIU DO CHAT!'
    print(f'{wlc_msg}\033[0m')

    with clients_lock:
        for client in clients:
            client.send(wlc_msg.encode(FORMAT))
    conn.send(help_msg.encode(FORMAT))
    try:
        connected = True
        while connected:
            # msg_len = int(conn.recv(HEADER).decode(FORMAT)) # dynamic message lenght
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            custom_msg = f"{datetime.now().strftime('%H:%M')} \033[1;{color}m[{name}]: {msg}\033[0m"
            print(custom_msg)
            with clients_lock:
                for client in clients:
                    client.sendall(custom_msg.encode(FORMAT))

    finally:
        print(f'{frwl_msg}\033[0m')
        with clients_lock:
            clients.remove(conn)
            for client in clients:
                client.sendall(frwl_msg.encode(FORMAT))
        conn.close()
    
start()