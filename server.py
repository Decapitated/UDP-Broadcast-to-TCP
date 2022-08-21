from ServerFinder import broadcastServer

UDP_GROUP = "230.0.0.0"
UDP_PORT = 5455
TCP_PORT = 5488
SECRET = "eb0492f0-1137-456e-a7ea-67a16e200f8c"

def start():
    print("Waiting for client...")
    client = broadcastServer(UDP_GROUP, UDP_PORT, TCP_PORT, SECRET)
    try:
        msg = None
        while msg != "Kill.":
            msg = input('Type Here: ')
            client.send(msg.encode())
    except ConnectionResetError:
        print("Client connection closed.")
        client.close()
        start()

start()