# Name: Guilherme Almeida Lopes
# Name: Hugo Okumura

# Create: 24-04-2025 
# Last modified: 27-04-2025

# Description: SocketClient class for the file system.
# This class is used to create a socket client that connects to the server.
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
  