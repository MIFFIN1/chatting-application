# Client script for chatting application

import socket, threading

HOST = '127.0.0.1'
PORT = 2673


def user_send_message(client):
    while True:
        message = input("Message: ")
        if message != " ":
            client.sendall(message.encode('utf-8'))
def listen_to_server(client):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != " ":
            username = message.split(":")[0]
            content = message.split(":")[1]
            print(f"[{username}]> {content}")

def communicate_to_server(client):
    username = input("Enter your name")
    client.sendall(username.encode())
    threading.Thread(target=listen_to_server.arg(client, )).start()
    user_send_message(client)

def main():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect(HOST,PORT)
    except:
        print("Can not connect to the server right now!")
    communicate_to_server(client)

if __name__ == "__main__":
    main()
