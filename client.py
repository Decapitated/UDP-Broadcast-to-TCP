import socket
import struct

UDP_GROUP = "230.0.0.0"
UDP_PORT = 5455
SERVER_SECRET = "eb0492f0-1137-456e-a7ea-67a16e200f8c"

def connectServer(addr, port: int):
    try:
        print("Connecting to server...")
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((addr, port))
        print("Connected to server.")
        tcp_socket.send(SERVER_SECRET.encode())
        while True:
            data = tcp_socket.recv(1024).decode()
            if(data == "Kill." or data == ""):
                print("Server closed.")
                break
            print("(TCP) "+data)
    finally:
        tcp_socket.close()

def start():
    print("Waiting for server...")
    #Setup UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.bind(("", UDP_PORT))
    mreq = struct.pack("=4sl", socket.inet_aton(UDP_GROUP), socket.INADDR_ANY)
    udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    try:
        connected = False
        while not connected:
            data, addr = udp_socket.recvfrom(1024)
            SECRET, PORT = tuple(data.decode().split(":"))
            if(SECRET == SERVER_SECRET):
                udp_socket.close()
                connected = True
                connectServer(addr[0], int(PORT))
    except ConnectionResetError as e:
        print("Server connection closed.")
        start()

if __name__ == "__main__":
    start()