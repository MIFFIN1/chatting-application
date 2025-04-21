# Client script for chatting application

import socket
import threading

HOST = '127.0.0.1'
PORT = 1234  # must match the server

def user_send_message(client):
    while True:
        message = input("Message: ")
        client.sendall(message.encode('utf-8'))
        if message == ".exit":
            print("Disconnected from chat.")
            client.close()                
            break

def listen_to_server(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if not message:
                break
            if ":" in message:
                username, content = message.split(":", 1)
                print(f"|{username}| {content}")
                if "Connected to server" not in message and "joined the chat" not in message:
                    client.sendall(f"RECEIVED from {username}".encode('utf-8'))
            else:
                print(message)
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except:
        print("Cannot connect to the server.")
        return

    threading.Thread(target=listen_to_server, args=(client,)).start()
    user_send_message(client)

if __name__ == "__main__":
    main()
