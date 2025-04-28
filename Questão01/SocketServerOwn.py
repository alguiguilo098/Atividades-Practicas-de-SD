
import socket
class ServerSocket:
    
    __socket=None

    def __init__(self, host:str, port:int,qtd_connect):
        # Create a socket server
        self.__socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the host and port
        self.__socket.bind((host, port))
        # Listen for incoming connections
        # Set the maximum number of queued connections
        self.__socket.listen(qtd_connect)
    
    def accept(self):
        # Accept an incoming connection
        # This method blocks until a connection is accepted
        return self.__socket.accept()
    
    def close(self):
        # Close the socket
        self.__socket.close()
    
   
