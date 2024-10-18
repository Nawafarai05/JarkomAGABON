import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("172.20.10.3", random.randint(8000, 9000)))

name = input("Username: ")
password = input("Password: ")


def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG: {name}:{password}".encode(), ("172.20.10.3", 9999))

while True:
    message = input("")
    if message == "exit":
        exit()
    else:
        client.sendto(f"{name}: {message}".encode(), ("172.20.10.3", 9999))
