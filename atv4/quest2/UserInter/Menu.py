from  SocketsUtil.SocketClient import SocketUDPClient
from SocketsUtil.BarUpload import BarUpload
import time
import sys
import os 
from hashlib import sha1

class ClientMenu:
    
    def __checksum(self,path):
        with open(path, "rb") as f:
            dados = f.read()
        hash_sha1 = sha1(dados).hexdigest()
        return hash_sha1
    
    def __send_data_file(self,path):
        with open(path, "rb") as f:
            while True:
                block=f.read(1024)
                self.__socket.sendto(block)
                time.sleep(0.5)
        print(bloco)

            
        
    
    def __send_metadata_file(self, namefile):
        abspath=os.path.join(self.__path,namefile)
        stat=os.stat("".join(abspath)).st_size
        filesize=str(stat)

        self.__barload=BarUpload([],(stat/1048)+3)
        name=abspath.split("/")[-1]
        nameandsize=name+":"+filesize
        
        self.__socket.sendto(nameandsize.encode())

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
        choice=int(input("Escolha uma opção: "))
        print("\n")

        self.__choices(choice)

    def __choices(self,choice):
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
        ip=input("IP: ")
        port=int(input("Port: "))
        self.__socket=SocketUDPClient(port,ip)
        print("Socket UDP Cliente Criado \n")

    def __list_file(self):
        direntry=os.listdir(self.__path)
        for i in direntry:
            filesize=os.stat(os.path.join(self.__path,i))
            print(f"nome:{i}    tamanho do arquivo:{filesize.st_size} Bytes    quantidade de pacotes (1024 bytes):{int((filesize.st_size/1024)+3)}")
        print("\n")

    def __send_file(self):
        namefile=input("Nome do Arquivo:")
        self.__send_metadata_file(namefile)

    def __close_client(self):
        print("Desalocando Recursos...")
        time.sleep(1)

        print("Desligando Conexeções...")
        time.sleep(1)

        sys.exit()

    def run(self):
        while True:
            self.__menu()