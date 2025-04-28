
import socket as sc

class SocketClient:
    socket=None

    def __init__(self):
        socket= sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        self.socket=socket
    def connect(self,host:str,port:int):
        self.socket.connect((host,port))
    def close(self):
        self.socket.close()
  