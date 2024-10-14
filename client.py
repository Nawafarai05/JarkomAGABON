import socket

# Membuat socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Menghubungkan ke server
client_socket.connect(('localhost', 49153))

# Mengirim data ke server
client_socket.sendall(b'Halo dari client!')

# Menerima data dari server
data = client_socket.recv(1024)
print(f"Dari server: {data.decode()}")

# Menutup koneksi
client_socket.close()
