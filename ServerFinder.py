import socket
import struct
from ServerBroadcast import ServerBroadcast

def broadcastServer(udp_group: str, udp_port: int, tcp_port: int, secret: str):
    server = ServerBroadcast(udp_group, udp_port, tcp_port, secret)
    awaitClient = server.startAwait()
    server.startMulticast()
    awaitClient.join()
    return server.client;

def findServer(udp_group: str, udp_port: int, secret: str):
    #Setup UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.bind(("", udp_port))
    mreq = struct.pack("=4sl", socket.inet_aton(udp_group), socket.INADDR_ANY)
    udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        data, addr = udp_socket.recvfrom(1024)
        SECRET, PORT = tuple(data.decode().split(":"))
        if(SECRET == secret):
            udp_socket.close()
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.connect((addr[0], int(PORT)))
            tcp_socket.send(secret.encode())
            return tcp_socket