from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from concurrent import futures
import mflix_pb2
import mflix_pb2_grpc
import grpc
from bson.objectid import ObjectId
'''
    *Nomes: Guilherme Almeida Lopes
    *Nomes: Hugo Okumura
    *Create: 30-05-2025
    * Last modified: 7-06-2025

    Este código em python implementa uma API, utilizando gRPC e protobufs, de gerenciamento de filmes.
    O servidor espera conexões externas de outros processos e responde a métodos como GET, POST, PUT e DELETE.
    Ao receber requisições com esses métodos ele acessa a um banco de dados utilizando MongoDB ATLAS para gerenciar os filmes. 
'''


'''
    Método que será envocado pelo gRPC e receberá conexões e gerenciá-las. 
    O método extende o objeto gerado pelo gRPC especificado no mflix.proto.
'''
class MovieServerRPC(mflix_pb2_grpc.FilmeServiceServicer):

    '''
        Método construtor que irá inicializar a conexão com o MongoDB
    '''
    def __init__(self):
        uri = "mongodb+srv://admin:admin@mflix.7jieeqw.mongodb.net/?retryWrites=true&w=majority&appName=Mflix"  
        # Substitua pelo URI real do MongoDB Atlas
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['Mflix']
        self.movies = self.db['movies']


    '''
        Método principal do serviço. Gerencia as requisições feitas por clientes.
        Retorna uma mesnagem de erro caso o tipo de requisição não é um tipo de requisição que a API está configurada a tratar. 
    '''
    def GerenciaFilmes(self, request, context):
        try:
            match request.tipo_requisicao:
                case mflix_pb2.FilmePedido.reqType.GET:
                    print("entrei no GET")
                    return self.get_filmes(request)
                case mflix_pb2.FilmePedido.reqType.POST:
                    print("entrei no POST")
                    response=self.post_filme(request)
                    print("cheguei no Post")
                    return response
                case mflix_pb2.FilmePedido.reqType.UPDATE:
                    print("entrei no UPDATE")
                    return self.update_filme(request)
                case mflix_pb2.FilmePedido.reqType.DELETE:
                    print("entrei no DELETE")
                    return self.delete_filme(request)
                case _:
                    return mflix_pb2.PedidoResposta(
                        mensagem="Tipo de requisição inválido",
                        sucesso=False
                    )
        except Exception as e:
            print(f'ErroCALVO: {e}')
            return mflix_pb2.PedidoResposta(
                mensagem=f"ERRO: {str(e)}",
                sucesso=False
            )

    '''
        Método GET do serviço.
        Nele, o cliente pode consultar os filmes que estão registrados no banco de dados.
        O cliente pode filtrar a lista de filmes retornados oferecendo uma lista de atores e/ou uma lista de generos.
    '''
    def get_filmes(self, request):
        query = {}
        if request.atores:
            query["atores"] = {"$in": list(request.atores)}
        if request.generos:
            query["generos"] = {"$in": list(request.generos)}

        filmes_lista = list(self.movies.find(query))
        if filmes_lista:
            return mflix_pb2.PedidoResposta(
                filmes=[self.doc_to_filme(f) for f in filmes_lista],
                mensagem=f"Encontrados {len(filmes_lista)} filmes",
                sucesso=True
            )
        else:
            return mflix_pb2.PedidoResposta(
                filmes=[],
                mensagem="Nenhum filme encontrado com os parâmetros propostos",
                sucesso=True
            )


    '''
        Método de POST do serviço.
        Nele, o cliente oference um objeto com todas as informações necessárias para adicionar um novo filme para o banco.
        Se ouver campos vazios na requisição o servidor irá gerar uma resposta de erro e informar os campos obrigatórios.
        Caso a criação seja bem sucedida o servidor irá gerar uma resposta de sucesso e o objeto adicionado para o cliente.
    '''
    def post_filme(self, request):
        campos_vazios = []
        print("comecei a validar os campos")
        if request.filme.titulo == "":
            campos_vazios.append("titulo")
        if not request.filme.diretores:
            campos_vazios.append("diretores")
        if not request.filme.atores:
            campos_vazios.append("atores")
        if not request.filme.generos:
            campos_vazios.append("generos")
        if request.filme.duracao == 0:
            campos_vazios.append("duracao")
        if request.filme.ano == 0:
            campos_vazios.append("ano")
        print(f"campos_vazios:{campos_vazios}")
        if campos_vazios:
            return mflix_pb2.PedidoResposta(
                mensagem=f"Solicitação recusada: campos {campos_vazios} são obrigatórios",
                sucesso=False
            )

        print(f"cheguei aqui")
        filme_documento = {
            "titulo": request.filme.titulo,
            "diretores": list(request.filme.diretores),
            "ano": request.filme.ano,
            "atores": list(request.filme.atores),
            "generos": list(request.filme.generos),
            "duracao": request.filme.duracao
        }

        print(f"cheguei aqui 1")
        result_id = self.movies.insert_one(filme_documento).inserted_id
        filme_inserido = self.movies.find_one({"_id": result_id})

        print(f"cheguei aqui 2")
        return mflix_pb2.PedidoResposta(
            filmes=[self.doc_to_filme(filme_inserido)],
            mensagem="Filme criado com sucesso",
            sucesso=True
        )

    '''
        Método de PUT do serviço.
        Nele, o cliente oferece um _id de um filme e um objeto com os campos
            a serem atualizados e as informações atualizadas do filme.
        Caso o _id não for um _id existente, o servidor irá gerar uma resposta de erro para o cliente.
        Caso bem sucedido, o servidor irá gerar uma resposta de sucesso e retornar o objeto com as informações atualizadas.
    '''
    def update_filme(self, request):
        if not request.filme.id:
            return mflix_pb2.PedidoResposta(
                mensagem="ID é obrigatório para a atualização",
                sucesso=False
            )

        update_data = {}
        if request.filme.titulo:
            update_data["titulo"] = request.filme.titulo
        if request.filme.diretores:
            update_data["diretores"] = list(request.filme.diretores)
        if request.filme.atores:
            update_data["atores"] = list(request.filme.atores)
        if request.filme.generos:
            update_data["generos"] = list(request.filme.generos)
        if request.filme.duracao:
            update_data["duracao"] = request.filme.duracao
        if request.filme.ano:
            update_data["ano"] = request.filme.ano

        result = self.movies.update_one(
            {"_id": ObjectId(request.filme.id)},
            {"$set": update_data}
        )

        filme_atualizado = self.movies.find_one({"_id": ObjectId(request.filme.id)})

        if result.modified_count > 0:
            return mflix_pb2.PedidoResposta(
                filmes=[self.doc_to_filme(filme_atualizado)],
                mensagem=f"Filme {request.filme.id} alterado com sucesso",
                sucesso=True
            )
        else:
            return mflix_pb2.PedidoResposta(
                filmes=[self.doc_to_filme(filme_atualizado)],
                mensagem="Nenhuma alteração foi realizada",
                sucesso=False
            )

    '''
        Método de DELETE do serviço.
        Nele, o cliente oferece um _id de filme para que seja deletado do banco de dados.
        Se o _id não for um existente, o servidor irá retornar uma mensagem de erro para o cliente.
        Caso exista o servidor irá deletar o filme do banco e retornar uma mensagem de bem sucedido.
    '''
    def delete_filme(self, request):
        if not request.filme.id:
            return mflix_pb2.PedidoResposta(
                mensagem="ID é obrigatório para exclusão",
                sucesso=False
            )

        result = self.movies.delete_one({"_id": ObjectId(request.filme.id)})
        if result.deleted_count > 0:
            return mflix_pb2.PedidoResposta(
                mensagem="Filme excluído com sucesso",
                sucesso=True
            )
        else:
            return mflix_pb2.PedidoResposta(
                mensagem="Nenhum filme foi removido",
                sucesso=False
            )

    '''
        Método que converte o formato de documento vindo do banco de dados para o formato do protobuf.
    '''
    def doc_to_filme(self, doc):
        return mflix_pb2.Filme(
            id=str(doc.get("_id", "")),
            titulo=doc.get("titulo", ""),
            ano=doc.get("ano", 0),
            duracao=doc.get("duracao", 0),
            diretores=doc.get("diretores", []),
            atores=doc.get("atores", []),
            generos=doc.get("generos", [])
        )

'''
    Função que configura o gRPC
'''
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # corrigido aqui
    mflix_pb2_grpc.add_FilmeServiceServicer_to_server(MovieServerRPC(), server)
    server.add_insecure_port("[::]:50051")
    print("Servidor iniciado na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
