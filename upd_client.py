import socket
import threading

# Buat koneksi ke server
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("localhost",9999)

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

# Jalankan thread untuk menerima pesan
t = threading.Thread(target=receive)
t.start()

logged = False
while logged == False:
    print("===== MENU =====")
    print("1. Login")
    print("2. Register")
    
    option = input("Choose option: ")

    if option == "1":  # Login
        username = input("Username: ")
        password = input("Password: ")
        client.sendto(f"LOGIN_TAG: {username}:{password}".encode(), ("localhost", 9999))

        message, _ = client.recvfrom(1024)
        response = message.decode()
        print(response)

        if not response.startswith("Invalid"):
            logged = True

    elif option == "2":  # Register
            username = input("Create username: ")
            password = input("Create password: ")
            client.sendto(f"REGISTER_TAG: {username}:{password}".encode(), ("localhost", 9999))
    
while True:
    message = input("")
    if message == "exit":
        exit()
    else:
        client.sendto(f"{username}: {message}".encode(), ("localhost", 9999))
