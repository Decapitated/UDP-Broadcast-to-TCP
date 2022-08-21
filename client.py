import socket

UDP_PORT = 5455
SERVER_SECRET = "eb0492f0-1137-456e-a7ea-67a16e200f8c"

def connectServer(addr, port: int):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((addr, port))
    tcp_socket.send(SERVER_SECRET.encode())
    while True:
        data = tcp_socket.recv(1024).decode()
        if(data == "Kill." or data == ""):
            print("Server closed.")
            break
        print("(TCP) "+data)

#Setup UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Set up socket to receieve broadcast
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udp_socket.bind(('127.0.0.1', UDP_PORT))

connected = False
while not connected:
    data = udp_socket.recv(1024).decode()
    SECRET, ADDRESS, PORT = tuple(data.split(":"))
    if(SECRET == SERVER_SECRET):
        connected = True
        connectServer(ADDRESS, int(PORT))