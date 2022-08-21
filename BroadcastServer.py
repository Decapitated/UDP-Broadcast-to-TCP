from numbers import Integral
from threading import Thread
from time import sleep
import socket
import utilities

class BroadcastServer:
    __broadcasting = False
    __connected = False
    client = None

    def __init__(self, udp_port: int, tcp_port: int, secret: str):
        self.UDP_PORT = udp_port
        self.TCP_PORT = tcp_port
        self.SECRET = secret

    def startBroadcast(self) -> Thread:
        thread = Thread(target=self.__broadcast)
        thread.start()
        return thread

    def startAwait(self) -> Thread:
        thread = Thread(target=self.__awaitConnect)
        thread.start()
        return thread

    def __broadcast(self):
        self.__broadcasting = True
        # Setup UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set up socket to send/receive broadcast
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        LOCAL_IP = utilities.getLocalIp()
        while self.__broadcasting:
            udp_socket.sendto(":".join([self.SECRET, LOCAL_IP, str(self.TCP_PORT)]).encode(), ("127.0.0.1", self.UDP_PORT))
            sleep(1)
    
    def __awaitConnect(self):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind(("0.0.0.0", self.TCP_PORT))
        tcp_socket.listen(100)
        while not self.__connected:
            tempClient, _addr = tcp_socket.accept()
            data = tempClient.recv(1024).decode()
            if(data != self.SECRET):
                tempClient.close()
                continue
            else:
                print("Client Connected!")
                self.__broadcasting = False
                self.__connected = True
                self.client = tempClient