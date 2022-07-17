import threading
import socket

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
    server.listen()
    while True:
        conn, addr = server.accept()
        with clients_lock: # Prevent multiple threads to modify "clients" simultaneously 
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # handling each client on a separated thread
        thread.start()



def handle_client(conn, addr):
    print(f'[SERVER] {addr} JOINED THE CHAT!')

    try:
        connected = True
        while connected:
            # msg_len = int(conn.recv(HEADER).decode(FORMAT)) # dynamic message lenght
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            print(f'[{addr}]: {msg}')
            with clients_lock:
                for client in clients:
                    client.sendall(f'[{addr}]: {msg}'.encode(FORMAT))


    finally:
        with clients_lock:
            clients.remove(conn)
            for client in clients:
                client.sendall(f'[SERVER] {addr} LEFT THE CHAT!')
        conn.close()
