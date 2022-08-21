from BroadcastServer import BroadcastServer

def start():
    print("Waiting for client...")
    server = BroadcastServer(5455, 5488, "eb0492f0-1137-456e-a7ea-67a16e200f8c")
    awaitClient = server.startAwait()
    server.startBroadcast()
    awaitClient.join()
    try:
        msg = None
        while msg != "Kill.":
            msg = input('Type Here: ')
            server.client.send(msg.encode())
    except ConnectionResetError:
        print("Client connection closed.")
        start()

start()