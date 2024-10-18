import socket
import threading
import queue

messages = queue.Queue()
clients = []
user_passwords = {}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("172.20.10.3", 9999))

valid_passwords = {
    "aliya": "cantik",
    "nana": "ganteng",
}

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
            decoded_message = message.decode()
            print(message.decode())

            if addr not in clients:

                if addr not in clients: 
                    if decoded_message.startswith("SIGNUP_TAG:"): 
                        _, credentials = decoded_message.split("SIGNUP_TAG: ", 1) 
                        username, password = credentials.split(":")
                        
                        if username in valid_passwords and valid_passwords[username] == password: 
                            clients.append(addr) 
                            user_passwords[addr] = username 
                            server.sendto(f"{username} joined!".encode(), addr) 
                        else: 
                            server.sendto("Invalid username or password!".encode(), addr) 
                    continue
               
                # clients.append(addr)
                # name = message.decode().split(":", 1)[-1]
                # server.sendto(f"{name} joined!".encode(), addr)
                                
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
