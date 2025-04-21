import threading
import socket
import random

host = '127.0.0.1' # localhost
port = 1234 # port number

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = {}

def broadcast(msg, excluded_client=None): 
    for client in clients:
        if client is not excluded_client:
            client.send(msg)

def handling(client):
    name = f"Client{random.randint(1, 9999)}"
    clients[client] = name
    welcome_msg = f'Connected to server, your assigned name is: {name}'.encode('utf-8')
    client.send(welcome_msg)
    # others = [n for s,n in clients.items() if s is not client]
    current_client = clients[client]
    rest_of_clients = []
    for socket, name in clients.items():
        if socket is not current_client:
            rest_of_clients.append(name)  
    if rest_of_clients:
        client.send(("Currently online: " + ", ".join(rest_of_clients)).encode())
    else:
        client.send(f"You're the only one here right now.".encode('utf-8'))
        
    broadcast(f'{name} has joined the chat.'.encode('utf-8'),excluded_client=client)
    # need to print client list part of work here, but for now imma leave it like this for  testing
    while True:
        #receive msg from client
        msg = client.recv(1024).decode('utf-8')
        if msg: #.exit command to disconnect
            if msg == ".exit":
                broadcast(f'Client {clients[client]}: disconnected.'.encode(), excluded_client=client)
                del clients[client]
                client.close()
                break
            elif msg.startswith("RECEIVED from"):
                print(f"{msg} (acknolwedge a message)")
            else: #broadcast msg to all clients
                print(f'Message from {clients[client]}: {msg}')
                broadcast(f'{clients[client]}: {msg}'.encode('utf-8'))
def receive(): #incoming connections
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        clients[client] = None  #placeholder until name is assigned
        thread = threading.Thread(target=handling, args=(client,))
        thread.start()


print("if you see this server is starting")
receive()
