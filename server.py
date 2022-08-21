from MulticastServer import MulticastServer

def start():
    print("Waiting for client...")
    server = MulticastServer("230.0.0.0", 5455, 5488, "eb0492f0-1137-456e-a7ea-67a16e200f8c")
    server.startMulticast()
    awaitClient = server.startAwait()
    awaitClient.join()
    try:
        msg = None
        while msg != "Kill.":
            msg = input('Type Here: ')
            server.client.send(msg.encode())
    except ConnectionResetError:
        print("Client connection closed.")
        server.close()
        start()

start()