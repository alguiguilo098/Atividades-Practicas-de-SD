from SocketsUtil.Log import Log
import socket
class SocketUDPServer:
    def __init__(self,port:int,ip:str):
        self.__socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.__socket.bind((ip,port))
        self.__logs=Log(path=f"./Server/Log/{ip}.log")
        self.__map={}
    def getfile(self):
        nameandsizefile=self.__recivebytes()
        self.__logs.writeInfo("GET NAME AND SIZE OF FILE")
        listmetadata=nameandsizefile.decode().split(":")
        self.__map["name"]=listmetadata[0]
        self.__map["size"]=listmetadata[1]

        

        print(self.__map)
    def __recivebytes(self):
        recive=self.__socket.recv(1024)
        self.__logs.writeInfo("GET PACKET UDP SIZE 1024")
        return recive
    def sendtoclient(msg:bytes):
        pass
 