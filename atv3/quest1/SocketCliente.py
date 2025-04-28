
import socket as sc

class SocketClient:
    socket=None 

    def __init__(self):
        # Create a socket client
        socket= sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        self.socket=socket
    def connect(self,host:str,port:int):
        # Connect to the server (host,port)
        self.socket.connect((host,port))
    def close(self):
        # Close the socket
        self.socket.close()
  