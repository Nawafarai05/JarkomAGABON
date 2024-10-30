import socket
import threading
import queue

# Antrian pesan dan daftar client yang terkoneksi
messages = queue.Queue()
clients = []
user_passwords = {}

# Setup server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))

# Fungsi untuk memuat pengguna dari file user_data.txt
def load_users_from_file():
    user_data = {}
    try:
        with open("user_data.txt", "r") as file:
            for line in file:
                line = line.strip()
                if not line or "," not in line:
                    continue
                parts = line.split(",", 1)
                if len(parts) == 2:
                    username, password = parts
                    user_data[username] = password
    except FileNotFoundError:
        pass  # Jika file belum ada, tidak masalah, nanti bisa dibuat
    return user_data

# Fungsi untuk menambahkan user baru ke file
def add_user_to_file(username, password):
    with open("user_data.txt", "a") as file:
        file.write(f"{username},{password}\n")

# Memuat user dari file saat server dijalankan
user_passwords = load_users_from_file()

# Fungsi untuk menambahkan user baru
def add_user(username, password):
    user_passwords[username] = password
    add_user_to_file(username, password)  # Simpan ke file

# Fungsi untuk mengecek apakah username tersedia
def is_username_available(username):
    return username not in user_passwords

# Fungsi untuk memvalidasi username dan password
def validate_login(username, password):
    return username in user_passwords and user_passwords[username] == password

# Fungsi untuk menerima pesan dari client
def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

# Fungsi untuk broadcast pesan ke semua client
def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            decoded_message = message.decode()
            print(decoded_message)

            # Handle register
            if decoded_message.startswith("REGISTER_TAG:"):
                _, credentials = decoded_message.split("REGISTER_TAG: ", 1)
                username, password = credentials.split(":")

                if is_username_available(username):
                    add_user(username, password)
                    server.sendto("Registration successful, please login now.".encode(), addr)
                else:
                    server.sendto("Username has been used, try another username.".encode(), addr)
                continue

            # Handle login
            if decoded_message.startswith("LOGIN_TAG:"):
                _, credentials = decoded_message.split("LOGIN_TAG: ", 1)
                username, password = credentials.split(":")

                if validate_login(username, password):
                    clients.append(addr)
                    server.sendto(f"You have joined the chat!".encode(), addr)
                else:
                    server.sendto("Invalid username or password, try again.".encode(), addr)
                continue
                

            # Broadcast pesan ke semua client yang sudah login
            for client in clients:
                if client != addr:
                    try:
                        server.sendto(message, client)
                    except Exception as e:
                        print(f"Error sending message to {client}: {e}")
                        if client in clients:
                            clients.remove(client)

# Jalankan thread untuk menerima dan broadcast pesan
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
