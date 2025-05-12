# Authors: Guilherme Almeida Lopes, Hugo Okumura
# Created: 12-05-2025
# Last Modified: 12-05-2025
#
# Description:
# ClientMenu is a command-line interface for sending files to a UDP server.
# It allows the user to set IP/port, view local files, send selected files (with progress bar),
# and ensures data integrity using SHA-1 checksum.

from  SocketsUtil.SocketClient import SocketUDPClient
from SocketsUtil.BarUpload import BarUpload
import time
import sys
import os 
from hashlib import sha1

class ClientMenu:
    
    def __checksum(self,path):
        """
            Get sha1 of file
        """
        with open(path, "rb") as f:
            dados = f.read()
        hash_sha1 = sha1(dados).digest() # calcualte sha1
        self.__socket.sendto(hash_sha1) # send to server
    
    def __send_data_file(self,path):
        """
            Send file to server
        """
        with open(path, "rb") as f:
            while True:
                block=f.read(1024)
                if not block:
                    break # leave loop,when no bytes reaad
                self.__socket.sendto(block) # send to sever 
                self.__barload.upload(1024) # up upload bar
                time.sleep(0.5)

            
        
    
    def __send_metadata_file(self, namefile):
        """
            Send to server file
        """
        abspath=os.path.join(self.__path,namefile) # get abspath of file
        stat=os.stat("".join(abspath)).st_size # get size file
        filesize=str(stat)
        self.__barload=BarUpload([],(stat/1048)+1) # create barupload 
        name=abspath.split("/")[-1] # split path
        nameandsize=name+":"+filesize
        self.__socket.sendto(nameandsize.encode()) # send file and size to server
        self.__barload.upload(1024)
        

    def __init__(self,pathmenu):
        self.__socket:SocketUDPClient=None
        self.__path:str=pathmenu
        self.__barload=None

    def __menu(self):
        print("Escolhas uma das opções a seguir\n")
        print("1- Escolher o IP e porta da máquina.")
        print("2- Enviar arquivo para o servidor")
        print("3- Listar os arquivos presentes no cliente")
        print("4- Fechar o cliente")

        print("\n")
        choice=int(input("Escolha uma opção: ")) # choice of user 
        print("\n")

        self.__choices(choice)

    def __choices(self,choice):
        """
            Logic choice 
        """
        if choice==1:
            self.__createsocket()
        elif choice==2 and self.__socket!=None:
            self.__send_file()
        elif choice==3 and self.__socket!=None:
            self.__list_file() 
        elif choice==4:
            self.__close_client()
        elif self.__socket==None:
            print("Defina o IP e Porta da maquina na opção 1\n")
        else:
            print("ERROR:Opção inválida")

    def __createsocket(self):
        """
            Socket create
        """
        ip=input("IP: ") 
        port=int(input("Port: "))
        self.__socket=SocketUDPClient(port,ip) # create socket UDP client 
        print("Socket UDP Cliente Criado \n")

    def __list_file(self):
        direntry=os.listdir(self.__path) # show all dirs in client
        for i in direntry:
            filesize=os.stat(os.path.join(self.__path,i)) # get size file
            print(f"nome:{i}    tamanho do arquivo:{filesize.st_size} Bytes    quantidade de pacotes (1024 bytes):{int((filesize.st_size/1024)+3)}")
        print("\n")

    def __send_file(self)->None:
        """
            Send bytes to server
        """
        namefile=input("Nome do Arquivo:")
        self.__send_metadata_file(namefile) # send metada
        pathabs=os.path.join(self.__path,namefile)
        self.__send_data_file(pathabs) # send file info bytes
        self.__checksum(pathabs) # send checksum image
        print(self.__socket.recive(1024).decode())
        
    def __close_client(self):
        """
            Cliente close conection
        """
        print("Desalocando Recursos...")
        time.sleep(1)
        print("Desligando Conexeções...")
        time.sleep(1)
        sys.exit() # finish client 

    def run(self):
        while True:
            # Run Menu 
            self.__menu ()