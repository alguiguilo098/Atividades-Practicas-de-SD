import socket
import struct
import os


'''

Autores: 
    Este código implementa o lado do cliente para o servidor de gerenciamento de arquivos.
    Ao executar o cliente irá conectar a um servidor e entrará em um loop infinito esperando input do usuário.
    Os inputs são:
        1/ADDFILE: adicionar um arquivo no diretório do servidor
        2/DELETE: remove um arquivo específico no diretório do servidor
        3/GETFILELIST: lista o nome e o tamanho de todos os arquivos do servidor
        4/GETFILE: faz o download de um arquivo do servidor e quarda no diretório do cliente
        5/SAIR: finaliza a conexão

    - Hugo Okumura
    - Guilherme Almeida Lopes 
Data Criação: 24/04/2025
Data Última Atualização: 28/04/2025
'''

class FileClient:

    def __init__(self, host='127.0.0.1', port=7777):
        self.host = host
        self.port = port
        self.client_files = './client_files'
        # Dicionário dos comandos
        self.cmd_dic = {
            "ADDFILE":0x01,
            "1":0x01,
            "DELETE":0x02,
            "2":0x02,
            "GETFILELIST":0x03,
            "3":0x03,
            "GETFILE":0x04,
            "4":0x04,
            "Sair":0x05,
            "5":0x05
        }
        # Cria o diretório de arquivos do cliente se não existir
        os.makedirs(self.client_files, exist_ok=True)

    '''
    Faz a conexão do cliente com o servidor.
    Espera o input do usuário para fazer solicitações ao servidor.
    '''
    def server_connect(self):

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host,self.port))
            while True:
                solicitacao = str(input(
f"\nO que deseja solicitar ao servidor?\n\
    (1)ADDFILE: adiciona arquivo novo\n\
    (2)DELETE: remove um arquivo existente\n\
    (3)GETFILELIST: retorna o nome de todos os arquivos\n\
    (4)GETFILE: faz o download de um arquivo\n\
    (5)SAIR: desconecta do servidor\n\
Formato de solicitação: 'código/nome da solicitação' 'nome do arquivo'\n\
Para operação (3) e (5) não é preciso do nome do arquivo\n\n->"
)).strip().split()
                
                cmd = solicitacao[0].upper()
                cmd = self.cmd_dic[cmd]

                filename = ""
                if len(solicitacao) > 1:
                    filename = solicitacao[1]

                filename_bytes = filename.encode('utf-8')
                '''
                ! = ordem big-endian
                B = unsigned byte de tamanho 1
                BBB = cada variável será atribuída um dado desempacotado no formato unsigned byte
                '''                
                # envia o cabeçalho de requisição (padrão para todos os comandos)
                if(cmd != 0x05):
                    header = struct.pack("!BBB", 0x01, cmd, len(filename))
                    self.client_socket.sendall(header+filename_bytes)
            
                match cmd:
                    case 0x01:
                        # envia a solicitação de adicionar um arquivo
                        self.add_file(self.client_socket, filename)
                    case 0x02:
                        # envia a solicitação de remover um arquivo
                        self.delete_file(self.client_socket)
                    case 0x03:
                        # envia a solicitação de listar todos os arquivos
                        self.get_file_list(self.client_socket)
                    case 0x04:
                        # envia a solicitação de download de um arquivo
                        self.get_file(self.client_socket, filename)
                    case 0x05:
                        # envia a solicitação de desconectar do servidor
                        self.client_socket.close()
                        break


        except Exception as e:
            print(f"Erro: {str(e)}")

    '''
    Envia a solicitação de enviar o arquivo ao servidor
    '''
    def add_file(self,client_socket,filename):
        try:
            file_path = os.path.join(self.client_files, filename)
            file_size = os.path.getsize(file_path)
            '''
            I = unsigned int de tamanho 4
            '''
            client_socket.sendall(struct.pack('!I', file_size))

            with open(file_path, 'rb') as f:
                while True:
                    byte = f.read(1)
                    if not byte:
                        break
                    client_socket.send(byte)

            self.read_response(client_socket, 0x01)
        
        except Exception as e:
            print(f"Erro ao enviar arquivo: {str(e)}")

    '''
    Envia a solicitação de remover um arquivo do servidor
    '''
    def delete_file(self,client_socket):
        self.read_response(client_socket, 2)


    '''
    Envia a solicitação de listar todos os arquivos
    '''
    def get_file_list(self,client_socket):
        try:
            response = client_socket.recv(3)

            message_type, command, status_code = struct.unpack('!BBB', response)

            if status_code == 1:
                n_file = struct.unpack('!H', client_socket.recv(2))[0]
                print(f"Lista de arquivos -- {n_file} arquivos encontrados")
                i = 1
                for _ in range(n_file):
                    filename_size = struct.unpack('!B', client_socket.recv(1))[0]
                    filename = client_socket.recv(filename_size).decode('utf-8')
                    print(f"{i} - {filename} ({filename_size}Bs)")
                    i+=1
            else:
                raise Exception(f"status_code = {status_code}")
        except Exception as e:
            print(f"Erro ao listar os arquivos: {str(e)}")


    '''
    Envia a solicitação de download de um arquivo do servidor
    '''
    def get_file(self,client_socket,filename):
        try:
            response = client_socket.recv(3)
            message_type, command, status_code = struct.unpack('!BBB', response)

            if status_code == 1:
                file_size = struct.unpack('!I', client_socket.recv(4))[0]

                download_path = os.path.join(self.client_files,filename)
                with open(download_path, 'wb') as f:
                    remaining = file_size
                    while remaining > 0:
                        byte = client_socket.recv(1)
                        if not byte:
                            break
                        f.write(byte)
                        remaining -= 1
                
                print(f"Arquivo {filename} baixado com sucesso")
            else:
                raise Exception(f"status_code: {status_code}")

        except Exception as e:
            print(f"Erro ao fazer o download do arquivo: {str(e)}") 
    
    '''
    Método padrão para aguardar a resposta do servidor
    '''
    def read_response(self, client_socket, expected_command):
        response = client_socket.recv(3)
        message_type, command_id, status_code = struct.unpack('!BBB', response)

        if command_id == expected_command:
            if status_code == 1:
                print("Operação realizada com sucesso")
            else:
                print("Erro na operação")
        else:
            print("Resposta inesperada do servidor")


if __name__ == '__main__':
    client = FileClient()
    client.server_connect()

