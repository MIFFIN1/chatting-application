import threading
import socket
import random

host = '127.0.0.1' # localhost
port = 1234 # port number

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = {}

def broadcast(msg): 
    for client in clients:
        client.send(msg)

def handling(client):
    name = f"Client{random.randint(1, 9999)}"
    clients[client] = name
    welcome_msg = f'Connected to server, your assigned name is : {name}'
    client.send(welcome_msg.encode('utf-8'))
    # need to print client list part of work here, but for now imma leave it like this for  testing
    while True:
        #receive msg from client
        msg = client.recv(1024).decode('utf-8')
        if msg: #.exit command to disconnect
            if msg == ".exit":
                print(f'Client {clients[client]} disconnected.')
                del clients[client]
                client.close()
                break
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
