from ServerFinder import findServer

UDP_GROUP = "230.0.0.0"
UDP_PORT = 5455
SERVER_SECRET = "eb0492f0-1137-456e-a7ea-67a16e200f8c"

def start():
    try:
        print("Looking for server...")
        server = findServer(UDP_GROUP, UDP_PORT, SERVER_SECRET)
        print("Connected to server.")
        while True:
            data = server.recv(1024).decode()
            if(data == "Kill." or data == ""):
                print("Server closed.")
                break
            print("(TCP) "+data)
    finally:
        server.close()


if __name__ == "__main__":
    try:
        start()
    except Exception as e:
        print(e)
        start()