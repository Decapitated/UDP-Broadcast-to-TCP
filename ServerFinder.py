from ast import Pass
from ServerBroadcast import ServerBroadcast

def broadcastServer(udp_group: str, udp_port: int, tcp_port: int, secret: str):
    server = ServerBroadcast(udp_group, udp_port, tcp_port, secret)
    awaitClient = server.startAwait()
    server.startMulticast()
    awaitClient.join()
    return server.client;

def findServer(udp_group: str, udp_port: int, secret: str):
    Pass