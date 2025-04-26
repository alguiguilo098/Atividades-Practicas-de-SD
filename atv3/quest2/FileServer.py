import logging
import os
from threading import Thread
import socket
import struct

'''
Descrição:
    Este código é para a implementação de um servidor de gerenciamento de arquivos.
    Ao executar, estará em um loop infinito esperando conexões de múltiplos clientes e suas solicitações.
    As solicitações aceitas são:
        (1) ADDFILE: adiciona um novo arquivo
        (2) DELETE: remove um arquivo existente
        (3) GETFILELIST: retorna uma lista com o nome dos arquivos
        (4) GETFILE: faz download de um arquivo

Autores: 
    - Hugo Okumura
    - 
Data Criação: 24/04/2025
Data Última Atualização: 
'''

def startLog():

    logging.basicConfig(
        level=logging.INFO,
        format="{asctime} - {levelname} - {message}",
        datefmt="%d-%m-%Y %H:%M",
        style="{",
        filename="./logs/logs.log",
        encoding="utf-8",
        filemode="a"
    )

class FileServer:


    def __init__(self, host='0.0.0.0', port=7777):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_dir = "./server_files"

        os.makedirs("./server_files",exist_ok=True)

    def start(self):
        self.server_socket.bind((self.host,self.port))
        self.server_socket.listen()

        logging.info(f"Server iniciado em {self.host}:{self.port}")
        print(f"Server iniciado. Esperando conexões em {self.host}:{self.port}")

        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                logging.info(f"Conexão realizada com {addr}")
                print(f"Conexão realizada com {addr}")
                client_thread = Thread(target=self.client_thread, args=(client_socket,))
                client_thread.start()

        except KeyboardInterrupt:
            logging.info(f"Servidor finalizado")
            self.server_socket.close()
    
    def client_thread(self, client_socket:socket):
        try:
            while True:
                header = client_socket.recv(3)
                if not header:
                    break
                
                '''
                ! = ordem big-endian
                B = unsigned byte de tamanho 1
                BBB = cada variável será atribuída um dado desempacotado no formato unsigned byte
                '''
                message_type, command, filename_size = struct.unpack("!BBB", header) 

                if message_type != 0x01:
                    self.response(client_socket, command, 2)
                    continue
                
                filename = client_socket.recv(filename_size).decode('utf-8')
                logging.info(f"Comando {command} recebido para arquivo: {filename}")
                print(f"Comando {command} recebido para arquivo: {filename}")

                match command:
                    case 0x01:
                        print("ok")
                        self.add_file(client_socket, filename)
                    case 0x02:
                        self.delete_file(client_socket, filename)
                    case 0x03:
                        self.get_file_list(client_socket)
                    case 0x04:
                        self.get_file(client_socket, filename) 
                    case _:
                        self.response()

        except Exception as e:
            logging.error(f"Erro no cliente: {str(e)}")

    def add_file(self, client_socket, filename):
        try:
            
            file_size_bytes = client_socket.recv(4)
            '''
            I = unsigned int de tamanho 4
            '''
            file_size = struct.unpack("!I", file_size_bytes)[0]
            
            file_path = os.path.join(self.server_dir,filename)
            with open(file_path, 'wb') as f:
                remaining = file_size
                while remaining > 0:
                    chunk = client_socket.recv(1)
                    if not chunk:
                        break
                    f.write(chunk)
                    remaining -= 1
            
            logging.info(f"Arquivo {filename} adicionado com sucesso")
            print(f"Arquivo {filename} adicionado com sucesso")
            self.response(client_socket,0x01,1)

        except Exception as e:
            logging.error(f"Erro ao adicionar arquivo {filename}: err {e}")
            self.response(client_socket, 0x01, 2)

    def delete_file(self, client_socket, filename):
        try:
            file_path = os.path.join(self.server_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"Arquivo {filename} removido com sucesso")
                print(f"Arquivo {filename} removido com sucesso")
                self.response(client_socket,0x02,1)
            else:
                logging.warning(f"Arquivo {filename} não existe")
                print(f"Arquivo {filename} não existe")
                self.response(client_socket,0x02,2)

        except Exception as e:
            logging.error(f"Erro ao excluir arquivo: {str(e)}")
            print(f"Erro ao excluir arquivo: {str(e)}")
            self.response(client_socket, 0x02, 2)

    def get_file_list(self, client_socket):
        try:
            files = os.listdir(self.server_dir)

            response = struct.pack('!BBB',0x02, 0x03,1)
            '''
            H = unsigned short de tamanho 2
            '''
            response += struct.pack('!H', len(files))

            for filename in files:
                filename_bytes = filename.encode('utf-8')
                response += struct.pack('!B', len(filename_bytes))
                response += filename_bytes
            
            client_socket.sendall(response)
            logging.info(f"Lista de arquivos enviada com sucesso")
            print(f"Lista de arquivos enviada com sucesso")

        except Exception as e:
            logging.error(f"Erro ao enviar lista de arquivos: {str(e)}")
            print(f"Erro ao enviar lista de arquivos: {str(e)}")
            self.response(client_socket,0x03,2)

    def get_file(self, client_socket, filename):
        try:
            file_path = os.path.join(self.server_dir, filename)
            if not os.path.exists(file_path):
                logging.warning(f"Arquivo {filename} não existe")
                self.response(client_socket,0x03,2)
                return
            
            file_size = os.path.getsize(file_path)

            response = struct.pack("!BBB", 0x02,0x04,1)
            response += struct.pack("!I", file_size)
            client_socket.sendall(response)

            with open(file_path, 'rb') as f:
                while True:
                    byte = f.read(1)
                    if not byte:
                        break
                    client_socket.send(byte)
            
            logging.info(f"Arquivo {filename} enviado com sucesso")
        
        except Exception as e:
            logging.error(f"Erro ao fazer o download de {filename}")
            print(f"Erro ao fazer o download de {filename}")
            self.response(client_socket,0x03,2)

    def response(self, client_socket, command, status_code):
        response = struct.pack("!BBB", 0x02, command, status_code)
        client_socket.sendall(response)

if __name__ == "__main__":
    os.makedirs("./logs", exist_ok=True)
    open("logs/logs.log","a+").close()
    startLog()
    server = FileServer()
    server.start()
