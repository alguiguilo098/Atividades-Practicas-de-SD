import socket

class SocketUDPClient:

    def __init__(self,port:int,ip:str):
        self.__socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.__port:int=port
        self.__ip:str=ip

    def sendto(self,packet:bytes):
        self.__socket.sendto(packet,(self.__ip,self.__port))

    def recive(self,buffersize):
        self.__buffer=self.__socket.recv(buffersize)
    
    def read_buffer(self,buffersize=None):
        return self.__buffer[:buffersize]