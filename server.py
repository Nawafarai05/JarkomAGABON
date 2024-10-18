import socket
import threading
import queue

messages = queue.Queue()
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("172.20.10.3", 9999))

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message.decode())

            if addr not in clients:
                clients.append(addr)
                name = message.decode().split(":", 1)[-1]
                server.sendto(f"{name} joined!".encode(), addr)
                
            for client in clients:

                if client != addr:
                    try :
                        server.sendto(message, client)
                    except Exception as e:
                        print(f"Error sending message to {client} : {e}")
                        if client in clients :
                            del clients[client]

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
