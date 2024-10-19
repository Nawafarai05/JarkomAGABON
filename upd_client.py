import socket
import threading
import random

# Buat koneksi ke server
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))

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

# Fungsi untuk menampilkan menu utama
def show_menu():
    print("===== MENU =====")
    print("1. Login")
    print("2. Register")
    print("3. Exit")

# Fungsi login
def login():
    username = input("Username: ")
    password = input("Password: ")
    client.sendto(f"LOGIN_TAG: {username}:{password}".encode(), ("localhost", 9999))

    while True:
        message = input("")
        if message.lower() == "exit":
            exit()
        else:
            client.sendto(f"{username}: {message}".encode(), ("localhost", 9999))

# Fungsi register
def register():
    while True:
        username = input("Create username: ")
        password = input("Create password: ")
        client.sendto(f"REGISTER_TAG: {username}:{password}".encode(), ("localhost", 9999))

        # Tunggu respons dari server apakah username tersedia atau tidak
        message, _ = client.recvfrom(1024)
        response = message.decode()
        print(response)

        if response == "Registration successful, please login now.":
            login()  # Setelah berhasil register, langsung diarahkan ke login
            break  # Keluar dari loop register
        else:
            print("Try again.")

while True:
    show_menu()
    option = input("Choose option: ")

    if option == "1":  # Login
        login()

    elif option == "2":  # Register
        register()

    elif option == "3":  # Exit
        print("Goodbye!")
        exit()

    else:
        print("Invalid option, please try again.")
