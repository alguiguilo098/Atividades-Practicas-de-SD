from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import socket
import threading
import mflix_pb2
import datetime
from bson import ObjectId

class MovieServer:
    def __init__(self, host='10.1.4.212', port=5000):

        '''Configurações do socket'''
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

        '''Configurações para o mongodb api'''
        uri = "mongodb+srv://admin:admin@mflix.xk8ftcw.mongodb.net/?retryWrites=true&w=majority&appName=mflix"
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['mflix']
        self.collection = self.db['movies']

    def run(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print("Servidor Iniciado esperando conexões..")
        try:
            while True:
                client, addr = self.socket.accept()
                print(f"Conexão com {addr} estabelecida")
                thread = threading.Thread(target=self.handle_connection, args=(client, addr))
                thread.start()

        except KeyboardInterrupt:
            print("Fechando conexão...")
            self.socket.close()
            self.client.close()
    
    def handle_connection(self, client, addr):
        
        try:
            while True:

                tamanho_bytes = client.recv(4)
                tamanho = int.from_bytes(tamanho_bytes, byteorder="big")
                pedido_empacotado = client.recv(tamanho)

                print(tamanho_bytes)
                print(pedido_empacotado)
                if len(pedido_empacotado) < tamanho:
                    print("Mensagem incompleta recebida")
                    '''Envia a Resposta de erro'''
                    self.send_response(False,cliente=client,filmes=None,mensagem="Erro no envio do pedido")
                    continue

                pedido = mflix_pb2.FilmePedido()
                pedido.ParseFromString(pedido_empacotado)
                print("CHEGUEI")
                match pedido.tipo_requisicao:
                    case 0:
                        print("get filmes")
                        self.get_filmes(pedido.atores,pedido.generos)
                    case 1:
                        print("create filmes")
                        self.create_filme(cliente=client,filme=pedido.filme,)
                    case 2:
                        print("atualizar filme")
                        self.update_filme(self, pedido.filme)
                    case 3: 
                        print("delte filme")
                        self.delete_filme(self, pedido.filme)    

        except Exception as e:
            print("socket calvo")
            print(e)

    def get_filmes(self, atores=[], generos=[]):

        query = {}
        message = "" 
        if atores:
            query["atores"] = {"$in": atores}
        if generos:
            query["generos"] = {"$in": generos}

        filmes_lista = list(self.collection.find(query))
        if len(filmes_lista) == 0:
            message = "Requisição sucedida: Banco de Dados vazio."
        else:
            message = "Requisição sucedida."

        self.send_response(True,filmes_lista,message)

    def create_filme(self,cliente,filme):
        campo_vazios = []
        
        if filme.titulo == "":
            campo_vazios.append("titulo")
        if filme.diretores == []:
            campo_vazios.append("diretores")
        if filme.atores == []:
            campo_vazios.append("atores")
        if filme.generos == []:
            campo_vazios.append("generos")
        if filme.duracao == None:
            campo_vazios.append("duracao")
        print(campo_vazios)
        if len(campo_vazios) > 0:
            error_msg = f"Erro ao criar filme: {campo_vazios} são necessários serem preenchidos"
            print("calvo")
            self.send_response(False,cliente=cliente,mensagem=error_msg)
            return
        print("cheguei aqui")
        filme_documento ={
            "titulo":filme.titulo,
            "diretores":list(filme.diretores),
            "ano": datetime.date.today().year,
            "atores": list(filme.atores),
            "generos": list(filme.generos),
            "duracao": filme.duracao,
        }
        print("opt opt")
        filme_inserido_id = self.collection.insert_one(filme_documento).inserted_id
        print("mongo")
        filme_inserido = self.collection.find_one({"_id": filme_inserido_id})
        if filme_inserido:
            mensagem = "Filme criado com sucesso"
            print(mensagem)
            self.send_response(True, filme_inserido, mensagem)
            print("Deu Certo Grande Calvo")
        else:
            print("calvo calvo")
            mensagem = "Erro ao criar a mensagem"
            self.send_response(False, filme_inserido, mensagem)

    def delete_filme(self, filme):
        
        if filme.id == "":
            self.send_response(False, filme,"ERRO DELETE: É necessário especificar um _id de filme")
            return

        filme_target = self.collection.delete_one({"_id":filme.id})

        if filme_target:
            pass
        else:
            self.send_response(True,filme,"DELETE: Não existe um filme com o _id oferecido")

    def update_filme(self, filme):
        campo_vazios = []
        
        if filme.id == "":
            campo_vazios.append("_id")
        if filme.titulo == "":
            campo_vazios.append("titulo")
        if filme.diretores == []:
            campo_vazios.append("diretores")
        if filme.atores == []:
            campo_vazios.append("atores")
        if filme.generos == []:
            campo_vazios.append("generos")
        if filme.duracao == None:
            campo_vazios.append("duracao")

        if len(campo_vazios) > 0:
            error_msg = f"Erro ao criar filme: {campo_vazios} são necessários serem preenchidos"
            self.send_response(False, mensagem=error_msg)
            return
        
        filme_editado = self.collection.find_one_and_update({"_id": filme.id}, filme)

        self.send_response(True,filme_editado)

    def send_response(self, sucesso,cliente, filmes=None, mensagem=None):
        pedido_resposta = mflix_pb2.PedidoResposta()
        pedido_resposta.sucesso = sucesso

        if mensagem:
            pedido_resposta.mensagem = mensagem
        
        if sucesso and filmes:
            # pedido_resposta.filme = 
            for f in filmes:
                filme = pedido_resposta.filme.add()
                filme.id = f.id
                filme.ano = f.ano
                filme.duracao = f.duracao
                filme.diretores.extend(f.diretores)
                filme.atores.extend(f.atores)
                filme.generos.extend(f.generos)

        
        resposta_byte = pedido_resposta.SerializeToString()
        cliente.sendall(len(resposta_byte).to_bytes(4, byteorder="big"))
        cliente.sendall(resposta_byte)


if __name__ == '__main__':
    m = MovieServer(host="192.168.237.134",port=5000)
    try:
        m.client.admin.command('ping') 
        # print('Monke')
    except Exception as e:
        print(e)

    m.run()


    # collection = db["movies"]
    # movie = {
    #     "plot":"Monke goes monke",
    #     "genre":["monke","banana"],
    #     "cast":["orangutan","chipamzee"],
    #     "title":"The monkee",
    #     "fullplot":"Ooh ooh ahh ahh, banana gib orangutan. But chipamzee ate banana instead",
    #     "countries":["behind you"],
    #     "released": datetime.datetime.now(tz=datetime.timezone.utc),
    #     "directors":["gorilla","baboon"],
    #     "rated":"UNRATED",
    #     "lastupdated": datetime.datetime.now(tz=datetime.timezone.utc),
    #     "year": 2025,
    #     "type": "movie"
    # }

    # # db_data = db.movies
    # # movie_id = db_data.insert_one(movie).inserted_id
    # # pprint.pprint(movie_id)
    # req = {"title":"The monkee"}
    # pprint.pprint(collection.find_one(req))


