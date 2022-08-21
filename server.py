from ServerFinder import broadcastServer

def start():
    print("Waiting for client...")
    client = broadcastServer("230.0.0.0", 5455, 5488, "eb0492f0-1137-456e-a7ea-67a16e200f8c")
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