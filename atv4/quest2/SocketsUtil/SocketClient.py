import socket
# Name: Guilherme Almeida Lopes
# Name: Hugo Okumura

# Create: 24-04-2025 
# Last modified: 27-04-2025

# Description:SocketUDPClient is a basic UDP client class that sends packets to a server and receives data,
#  using a specified IP and port.


class SocketUDPClient:

    def __init__(self,port:int,ip:str):
        """
            Constructor SocketClient       
        """
        self.__socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
        self.__port:int=port #Port
        self.__ip:str=ip #IP

    def sendto(self,packet:bytes):
        """
            Send packet to Client 
        """
        self.__socket.sendto(packet,(self.__ip,self.__port))

    def recive(self,buffersize):
        """
            recive data of server
        """
        return self.__socket.recv(buffersize)