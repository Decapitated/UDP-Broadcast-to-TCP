from threading import Thread
from time import sleep
import socket
import utilities

class MulticastServer:
    __multicasting = False
    __connecting = False
    client = None

    def __init__(self, udp_group: str, udp_port: int, tcp_port: int, secret: str):
        self.UDP_GROUP = udp_group
        self.UDP_PORT = udp_port
        self.TCP_PORT = tcp_port
        self.SECRET = secret

    def close(self):
        self.__multicasting = False
        self.__connecting = False
        self.client.close()

    def startMulticast(self) -> Thread:
        thread = Thread(target=self.__multicast)
        thread.start()
        return thread

    def startAwait(self) -> Thread:
        thread = Thread(target=self.__awaitConnect)
        thread.start()
        return thread

    def __multicast(self):
        self.__multicasting = True
        # Setup UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set up socket to send multicast
        udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        LOCAL_IP = utilities.getLocalIp()
        udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(LOCAL_IP))
        while self.__multicasting:
            udp_socket.sendto(":".join([self.SECRET, str(self.TCP_PORT)]).encode(), (self.UDP_GROUP, self.UDP_PORT))
            sleep(1)
        udp_socket.close()

    def __awaitConnect(self):
        self.__connecting = True
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Use 0.0.0.0 for tcp or connection will be refused.
        tcp_socket.bind(("0.0.0.0", self.TCP_PORT))
        tcp_socket.listen()
        while self.__connecting:
            tempClient = tcp_socket.accept()[0]
            data = tempClient.recv(1024).decode()
            if(data != self.SECRET):
                tempClient.close()
                continue
            else:
                print("Client Connected!")
                self.__multicasting = False
                self.__connecting = False
                self.client = tempClient
        tcp_socket.close()