import socket
import threading

# Buat koneksi ke server
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("localhost", 9999)
logged = False

def receive():
    global logged
    while logged:  # hanya menerima pesan setelah login berhasil
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_messages():
    global logged
    while logged:
        message = input("")
        if message == "exit":
            client.close()  # Menutup socket sebelum keluar
            break
        else:
            client.sendto(f"{username}: {message}".encode(), address)

# Login atau registrasi
while not logged:
    print("===== MENU =====")
    print("1. Login")
    print("2. Register")
    
    option = input("Choose option: ")

    if option == "1":  # Login
        username = input("Username: ")
        password = input("Password: ")
        client.sendto(f"LOGIN_TAG: {username}:{password}".encode(), address)

        message, _ = client.recvfrom(1024)
        response = message.decode()
        print(response)

        if not response.startswith("Invalid"):
            logged = True
            # Mulai menerima pesan setelah login
            t_receive = threading.Thread(target=receive)
            t_receive.start()
            # Mulai mengirim pesan setelah login
            t_send = threading.Thread(target=send_messages)
            t_send.start()

    elif option == "2":  # Register
        username = input("Create username: ")
        password = input("Create password: ")
        client.sendto(f"REGISTER_TAG: {username}:{password}".encode(), address)
        
        # Immediately receive and display the server response
        message, _ = client.recvfrom(1024)
        response = message.decode()
        print(response)

    
while True:
    message = input("")
    if message == "exit":
        exit()
    else:
        client.sendto(f"{username}: {message}".encode(), ("localhost", 9999))
