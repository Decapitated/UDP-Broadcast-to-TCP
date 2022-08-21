from ast import Pass
from MulticastServer import MulticastServer

def broadcastServer(udp_group: str, udp_port: int, tcp_port: int, secret: str):
    server = MulticastServer(udp_group, udp_port, tcp_port, secret)
    awaitClient = server.startAwait()
    server.startMulticast()
    awaitClient.join()
    return server.client;

def findServer(udp_group: str, udp_port: int, secret: str):
    Pass