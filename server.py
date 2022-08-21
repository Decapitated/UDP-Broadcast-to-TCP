from BroadcastServer import BroadcastServer

def start():
    print("Waiting for client...")
    server = BroadcastServer(5455, 5488, "Cheese Fries!")
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