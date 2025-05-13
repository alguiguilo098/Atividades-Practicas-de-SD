import socket
import struct
import emoji
from threading import Thread

'''
Autores: 
    - Hugo Okumura
    - Guilherme Almeida Lopes 
Data Criação: 9/05/2025
Data Última Atualização: 12/05/2025

    Este código implmenta uma conexão p2p utilizando o protocolo de rede UDP. Ao executar
    o usuário deve preencher seu nickname, endereço de IP e PORT conforme pedido. Ao fazer isso
    irá iniciar uma interface de chat com os comandos:
        - /conectar <IP> <PORT>: "conecta" com um outro peer para conseguir realizar a comunicação
        - /msg <message>: envia uma mensgaem para todos os peers
        - /emoji <:emoji:>: envia um emoji para todos os peers
        - /echo: envia uma mensagem "PING" para todos os peers que irá fazer com que todos gerem uma resposta "PONG" para indicar se está ativo
        - /sair: finaliza a interface e o processo
'''

class UDPPeer:

    def __init__(self, nickname, host, port):
        self.nickname = nickname
        self.nick_size = len(self.nickname)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.peers = set()
        self.running = True
    
    def run(self):
        '''
        Processo principal do peer. Aqui o usuário irá receber um prompt para o comando para a comunicação com outros peers.
        '''
        self.sock.bind((self.host, self.port))
        print(f"Server iniciado. Esperando conexões em {self.host}:{self.port}")
        self.listen = Thread(target=self.receive_thread)
        self.listen.daemon = True
        self.listen.start()

        print("Comandos disponíveis:")
        print("/conectar <IP> <PORT> - Conectar a outro peer")
        print("/msg <mensagem> - Enviar texto")
        print("/emoji <emoji> - Enviar emoji")
        print("/url <link> - Enviar URL")
        print("/echo - Enviar ECHO")
        print("/sair - Encerrar")
        # Enviando mensagens
        try:
            while self.running:

                cmd = input("\n> ").strip().split(' ', 1)
                
                match cmd[0]:
                    case "/conectar":
                        ip, port= cmd[1].split()
                        self.connect_peer(ip, int(port))
                    case "/msg": # mensagem normal
                        self.send_message(1, cmd[1])
                    case "/emoji": # emoji
                        self.send_message(2,cmd[1])
                    case "/url": # URL
                        self.send_message(3,cmd[1])
                    case "/echo": # ECHO
                        self.send_message(4,"PING")
                    case "/sair":
                        self.sock.close()
                        self.running = False
                        print("Encerrado")
        except KeyboardInterrupt:
            self.running = False
            self.sock.close()
    
    def receive_thread(self):
        '''
        Thread onde o peer irá receber e processar as mensagens de outros peers
        '''
        while self.running:

            try:
                data, addr = self.sock.recvfrom(1024)
                if len(data) < 3:
                    continue

                msg_type, nick_size = struct.unpack('!BB', data[:2])
                nickname = data[2:nick_size+2].decode('utf-8')
                msg_size = data[nick_size+2]
                
                if len(data) < 3 + nick_size + msg_size:
                    continue

                message = data[2+nick_size+1:2+nick_size+1+msg_size].decode('utf-8')

                print(f"{data}")

                if msg_type == 4:
                # Se receber uma mensagem de ECHO irá responder com a confirmação que está ativo
                    if message == "PING":
                        ative_message = "PONG"
                        response = struct.pack("!BB",4, self.nick_size)
                        response = self.nickname.encode('utf-8')
                        response += struct.pack("!B", len(ative_message))
                        response += ative_message.encode('utf-8')
                        print(f"Recebido mensagem ECHO de {addr}: eviando {ative_message}")
                        self.send_message(msg_type=4,message=ative_message, dest=addr)

                # Se receber uma resposta do ECHO enviado irá printar que o usuário está conectado
                    else:
                        print(f"{nickname} está ativo")
                else:
                    if msg_type == 2:
                        print(emoji.emojize(f"{nickname}: {message}"))
                    else:
                        print(f"{nickname}: {message}")

            except Exception as e:
                print(f"{e}")

    def connect_peer(self, peer_ip, peer_port):
        '''Conecta com outro peer'''
        try:
            self.peers.add((peer_ip, peer_port))
            print(f"Conectado a {peer_ip}:{peer_port}")
            print(self.peers)
        except Exception as e:
            print(f"{e}")

    def send_message(self, msg_type, message, dest=None):
        '''Método de envio de mensagens'''
        try:
            header = struct.pack("!BB", msg_type, self.nick_size)
            header += self.nickname.encode('utf-8')
            header += struct.pack("!B", len(message))
            header += message.encode('utf-8')
            print(header)
            if dest:
                self.sock.sendto(header,dest)
            else:
                for peer in self.peers:
                    self.sock.sendto(header,peer)

        except Exception as e:
            print(f"{e}")

    

if __name__ == "__main__" :
    nickname = input("Informe um nickname: ")
    ip = input("Informe o seu IP: ")
    port = int(input("Informe o seu PORT: "))

    s = UDPPeer(nickname=nickname, host=ip, port=port)

    try:
        s.run()
    except Exception as e:
        print(f"{e}")


