
import socket
class ServerSocket:
    
    __socket=None

    def __init__(self, host:str, port:int,qtd_connect):
        self.__socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((host, port))
        self.__socket.listen(qtd_connect)
    
    def accept(self):
        return self.__socket.accept()
    
    def close(self):
        self.__socket.close()
    
   
