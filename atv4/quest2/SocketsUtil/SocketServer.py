
from SocketsUtil.Log import Log
import socket
import os
from hashlib import sha1
# Name: Guilherme Almeida Lopes
# Name: Hugo Okumura

# Create: 24-04-2025 
# Last modified: 27-04-2025

# Description:SocketUDPServer is a simple UDP-based server that receives files from a client, 
# logs events, validates the file integrity using SHA-1 checksum, and confirms successful transfer 
# or error to the client.

class SocketUDPServer:
    """
        Socket UDP Server 
    """
    def __init__(self:object,port:int,ip:str):

        """
            Constructor class SocketUDPServer
        """
        self.__socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # create socket UDP
        self.__socket.bind((ip,port)) # configuration server port and ip
        self.__logs=Log(path=f"./Server/Log/{ip}.log") # Create Log
        self.__client_info=None # cliente address
        self.__map={} # info file

    
    def getfile(self)->None:
        """
            Get file of client and upload to server
        """    
        nameandsizefile=self.__recivebytes()
        self.__get_metadata_file(nameandsizefile) 
        self.__get_bytes_of_file()  
        self.__get_chucksum_packet() 
        self.__comparechecksum()  
        
    
    def __get_chucksum_packet(self):
        """
            Calculete chucksum of byte arrive client
        """
        self.__map["file"]=open(f"./Server/Images/{self.__map["name"]}","rb")
        filechuck=self.__map["file"].read()
        self.__map["sha1"]=sha1(filechuck).hexdigest()

    
    def __get_bytes_of_file(self):
        """
        
        """
        self.__map["file"]=open(f"./Server/Images/{self.__map["name"]}","wb")
        i=0
        while i<self.__map["size"]:
            block=self.__recivebytes()
            self.__map["file"].write(block)
            i+=1024
        self.__map["file"].close()
        self.__map.pop("file")
    
    def __comparechecksum(self):
        """
            Compare chuncksum client image and server
            return to client mensage SUCESS or ERROR
        """
        sha1_client=self.__recivebytes() # recive one packet
        if self.__map["sha1"]==sha1_client.hex():
            self.__logs.writeInfo("FILE TRANSFER OK") 
            self.__map["file"].close() # close file 
            self.__sendtoclient("SUCESS\n\n".encode()) # send to client, status sucess 
        else:
            # erro calculate checksum
            self.__logs.writeError("FILE TRANSFER ERROR")
            os.remove(self.__map["file"]) # remove file
            self.__sendtoclient("ERROR".encode()) # send ERROR mensage to client

    def __get_metadata_file(self, nameandsizefile):
        """
            get metadatas of file, send to server
        """
        listmetadata=nameandsizefile.decode().split(":") # split name and size
        self.__logs.writeInfo(f"GET NAME FILE:{listmetadata[0]}") # write action in log file
        self.__map["name"]=listmetadata[0] 
        self.__map["size"]=int(listmetadata[1])
    
    
    def __recivebytes(self):
        """
            recive one packet of 1024 bytes
        """
        recive,self.__client_info=self.__socket.recvfrom(1024)
        self.__logs.writeInfo("GET PACKET UDP SIZE 1024")
        return recive

    def __sendtoclient(self,msg:bytes):
        """
            send mensage to client 
        """
        self.__socket.sendto(msg,self.__client_info)