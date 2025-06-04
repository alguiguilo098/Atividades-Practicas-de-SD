from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import socket
import threading
import mflix_pb2
import datetime
from bson import ObjectId

# Name: Guilherme Almeida Lopes
# Name: Hugo Okumura
# Create: 16-05-2025
# Last modified: 21-05-2025
# This code implements a TCP server that listens for movie-related requests (such as retrieving,
# creating, updating, and deleting movies) using MongoDB as the database.

# MongoDB connection settings
uri="mongodb+srv://admin:admin@mflix.7jieeqw.mongodb.net/?retryWrites=true&w=majority&appName=Mflix"


class MovieServer:
    def __init__(self, host="0.0.0.0", port=5000):
        # Socket configuration
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['Mflix']
        self.collection = self.db['movies']

    def run(self):
        # Bind and listen on the specified host and port
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print("Server started, waiting for connections...")
        try:
            while True:
                client, addr = self.socket.accept()
                print(f"Connection established with {addr}")
                # Each client is handled in a new thread
                thread = threading.Thread(target=self.handle_connection, args=(client, addr))
                thread.start()
        except KeyboardInterrupt:
            print("Shutting down server...")
            self.socket.close()
            self.client.close()

    def handle_connection(self, client, addr):
        try:
            while True:
                # Read the size of the incoming request (4 bytes)
                tamanho_bytes = client.recv(4)
                tamanho = int.from_bytes(tamanho_bytes, byteorder="big")
                pedido_empacotado = client.recv(tamanho)
                print("OK")
                if len(pedido_empacotado) < tamanho:
                    # Incomplete request received
                    self.send_response(False, cliente=client, filmes=None, mensagem="Incomplete request received.")
                    continue
                
                pedido = mflix_pb2.FilmePedido()
                pedido.ParseFromString(pedido_empacotado)
                # Handle request type
                match pedido.tipo_requisicao:
                    case 0:
                        self.get_filmes(cliente=client,atores=list(pedido.atores),generos=list(pedido.generos))
                    case 1:
                        self.create_filme(cliente=client, filme=pedido.filme)
                    case 2:
                        self.update_filme(cliente=client,filme=pedido.filme)
                    case 3: 
                        self.delete_filme(cliente=client,filme=pedido.filme)
        except Exception as e:
            print(e)
            
        

    def get_filmes(self,cliente, atores=[], generos=[]):
        # Build MongoDB query based on filters
        query = {}
        if atores:

            query["atores"] = {"$in": atores}
        if generos:
            query["generos"] = {"$in": generos}

        filmes_lista = list(self.collection.find(query))
        message = "Request successful." if filmes_lista else "Request successful: No records found."
        self.send_response(True,cliente=cliente,filmes=filmes_lista,mensagem=message)
        self.send_response(True,cliente=cliente,filmes=filmes_lista,mensagem=message)

    def create_filme(self, cliente, filme):
        # Validate required fields
        campo_vazios = []
        if filme.titulo == "":
            campo_vazios.append("titulo")
        if not filme.diretores:
            campo_vazios.append("diretores")
        if not filme.atores:
            campo_vazios.append("atores")
        if not filme.generos:
            campo_vazios.append("generos")
        if filme.duracao == 0:
            campo_vazios.append("duracao")

        if campo_vazios:
            error_msg = f"Error: The following fields are required: {campo_vazios}"
            self.send_response(False, cliente=cliente, mensagem=error_msg)
            return
        
        # Build MongoDB document
        filme_documento = {
            "titulo": filme.titulo,
            "diretores": list(filme.diretores),
            "ano": datetime.date.today().year,
            "atores": list(filme.atores),
            "generos": list(filme.generos),
            "duracao": filme.duracao,
        }
        print("inicializar")
        # Insert and fetch new movie
        filme_inserido_id = self.collection.insert_one(filme_documento).inserted_id
        print("insert one")
        filme_inserido = self.collection.find_one({"_id": filme_inserido_id})
        print("find one")
        mensagem = "Movie successfully created" if filme_inserido else "Failed to create movie"
        self.send_response(filme_inserido is not None, cliente, [filme_inserido] if filme_inserido else None, mensagem)
        print("tudo certo")

    def delete_filme(self,cliente,filme):
        if filme.id == "":
            self.send_response(False, None, mensagem="DELETE ERROR: Movie _id is required")
            return

        # Delete by ID
        filme_target = self.collection.delete_one({"_id": ObjectId(filme.id)})
        if filme_target.deleted_count == 0:
            self.send_response(True,cliente,None, mensagem="DELETE: No movie found with the provided _id")
            self.send_response(True,cliente,None, mensagem="DELETE: No movie found with the provided _id")
        else:
            self.send_response(True,cliente, None,mensagem="Movie successfully deleted")
            self.send_response(True,cliente, None,mensagem="Movie successfully deleted")

    def update_filme(self,cliente,filme):
        campo_vazios = []
        if filme.id == "":
            campo_vazios.append("_id")
        if filme.titulo == "":
            campo_vazios.append("titulo")
        if not filme.diretores:
            campo_vazios.append("diretores")
        if not filme.atores:
            campo_vazios.append("atores")
        if not filme.generos:
            campo_vazios.append("generos")
        if filme.duracao == 0:
            campo_vazios.append("duracao")

        if campo_vazios:
            error_msg = f"Error: The following fields are required: {campo_vazios}"
            self.send_response(False, None,cliente, mensagem=error_msg)
            self.send_response(False, None,cliente, mensagem=error_msg)
            return

        # Update movie
        update_data = {
            "titulo": filme.titulo,
            "diretores": list(filme.diretores),
            "atores": list(filme.atores),
            "generos": list(filme.generos),
            "duracao": filme.duracao,
        }

        filme_editado = self.collection.find_one_and_update({"_id": ObjectId(filme.id)}, {"$set": update_data}, return_document=True)
        self.send_response(True,cliente=cliente ,filmes=[filme_editado] if filme_editado else None, mensagem="Movie updated")

    def send_response(self, sucesso, cliente, filmes=None, mensagem=None):
        pedido_resposta = mflix_pb2.PedidoResposta()
        pedido_resposta.sucesso = sucesso
        print("teste")
        if mensagem:
            pedido_resposta.mensagem = mensagem
        print("movie list")
        # Serialize movie list into response
        if sucesso and filmes:
            for f in filmes:
                filme_pb = pedido_resposta.filmes.add()
                filme_pb.id = str(f["_id"])
                filme_pb.titulo = f["titulo"]
                filme_pb.ano = f["ano"]
                filme_pb.duracao = f["duracao"]
                filme_pb.diretores.extend(f["diretores"])
                filme_pb.atores.extend(f["atores"])
                filme_pb.generos.extend(f["generos"])
        resposta_byte = pedido_resposta.SerializeToString()
    
        print(type(resposta_byte))
        size = len(resposta_byte)
        print(size)

        # Envia corretamente os 4 bytes do tamanho
        cliente.sendall(size.to_bytes(4, byteorder="big"))
        print("send")
        print("send")
        # Envia a mensagem serializada
        cliente.sendall(resposta_byte)


# Entry point
if __name__ == '__main__':
    m = MovieServer()
    try:
        m.client.admin.command('ping')
    except Exception as e:
        print(e)

    m.run()
