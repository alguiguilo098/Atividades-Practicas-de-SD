import socket

class SocketUDPClient:

    def __init__(self,port:int,ip:str)->object:
        self.__socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.__port:int=port
        self.__ip:str=ip

    def sendto(self,packet:bytes):
        self.__socket.sendto(packet,(self.__ip,self.__port))

    def recive(self,buffersize):
        return self.__socket.recv(buffersize)