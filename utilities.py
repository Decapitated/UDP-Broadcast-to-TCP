import socket

def getLocalIp():
    return socket.gethostbyname_ex(socket.getfqdn())[2][0]
