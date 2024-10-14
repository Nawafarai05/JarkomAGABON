import socket

# Membuat socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Mengikat socket ke alamat dan port
server_socket.bind(('localhost', 49153))

# Mendengarkan koneksi
server_socket.listen()

print("Menunggu koneksi...")
client_socket, addr = server_socket.accept()
print(f"Koneksi dari {addr}")

# Menerima data dari client
data = client_socket.recv(1024)
print(f"Dari client: {data.decode()}")

# Mengirim data ke client
client_socket.sendall(b'Halo dari server!')

# Menutup koneksi
client_socket.close()
server_socket.close()
