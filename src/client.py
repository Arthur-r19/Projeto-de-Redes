from cgitb import text
import threading
import socket
import textwrap

PORT = 5050
SERVER = "localhost" # socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
# HEADER = 64
DISCONNECT_MESSAGE = "!CLOSE"
CLEAR_MESSAGE = "!CLEAR"
HELP_MESSAGE = "!HELP"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPV4 Adresses with TCP protocol
    client.connect(ADDRESS)
    return client

def send(client, msg):
    client.sendall(msg.encode(FORMAT))

def listen_messages(conn):
    while True:
        msg = conn.recv(1024).decode(FORMAT)
        if not msg:
            break
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
            if msg == CLEAR_MESSAGE:
                print('\033[1J\033[1;1H', end='')
                continue
            if msg == HELP_MESSAGE:
                print(textwrap.dedent("""\
                LISTA DE COMANDOS DISPONÍVEIS:
                \033[1;31m!CLEAR\033[0m\t\t \033[2mLimpa a tela do terminal\033[0m
                \033[1;31m!CLOSE\033[0m\t\t \033[2mEncerra a sala de bate-papo\033[0m
                \033[1;31m!HELP\033[0m\t\t \033[2mAbre a lista de comandos disponíveis\033[0m"""))
                continue
            
            send(conn, msg)
        
        send(conn, DISCONNECT_MESSAGE)
    finally:
            pass

start()