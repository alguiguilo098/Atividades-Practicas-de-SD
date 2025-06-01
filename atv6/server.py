from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from concurrent import futures
import grpc
import mflix_pb2
import mflix_pb2_grpc
from bson.objectid import ObjectId

class MovieServerRPC(mflix_pb2_grpc.FilmeServiceServicer):
    
    def __init__(self):
        uri = "mongoatlasurl"
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['Mflix']
        self.movies = self.db['movies']

    def GerenciaFilmes(self, request, context):
        # return super().GerenciaFilmes(request, context)
        try:
            match request.tipo_requisicao:
                case mflix_pb2.GET:
                    pass
                case mflix_pb2.POST:
                    pass
                case mflix_pb2.UPDATE:
                    pass
                case mflix_pb2.DELETE:
                    pass
                case _:
                    return mflix_pb2.PedidoResposta(
                        mensagem="Tipo de requisição inválido",
                        sucesso=False
                    )
        except Exception as e:
            print(f'Erro: {e}')
            return mflix_pb2.PedidoResposta(
                mensagem=f"ERRO: {str(e)}",
                sucesso=False
            )

    def get_filmes(self, request):
        query = {}
        if request.atores:
            query["atores"] = {"$in": request.atores}
        if request.generos:
            query["generos"] = {"$in": request.generos}

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
                mensagem=f"Nenhum filme encontrado com os parâmetros propostos",
                sucesso=True
            )
        
    def post_filme(self,request):
        campos_vazios = []
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

        if campos_vazios:
            return mflix_pb2.PedidoResposta(
                mensagem=f"Solicitação recusada: campos {campos_vazios} são obrigatórios",
                sucesso=False
            )
        
        filme_documento = {
            "title" : request.filme.titulo,
            "diretores" : list(request.filme.diretores),
            "ano" : request.filme.ano,
            "atores" : list(request.filme.atores),
            "generos" : list(request.filme.generos),
            "duracao" : request.filme.duracao
        }

        result = self.movies.insert_one(filme_documento)
        result = self.movies.find_one({"_id":result}),
        return mflix_pb2.PedidoResposta(
            filme=result,
            mensagem=f"Filme criado com sucesso \n {result}",
            sucesso=True
        )
    
    def update_filme(self, request):
        if not request.filme.id:
            return mflix_pb2.PedidoResposta(
                mensagem="ID é obrigatório para a atualização",
                sucesso=False
            )
        
        update_data = {}
        if request.filme.titulo:
            update_data["titulo"] = request.filme.titulo
        if not request.filme.diretores:
            update_data["diretores"] = list(request.filme.diretores)
        if not request.filme.atores:
            update_data["atores"] = list(request.filme.atores)
        if not request.filme.generos:
            update_data["generos"] = list(request.filme.generos)
        if request.filme.duracao:
            update_data["duracao"] = request.filme.duracao
        if request.filme.ano:
            update_data["ano"] = request.filme.ano

        result = self.movies.update_one(
            {"_id": ObjectId(request.filme.id)},
            {"$set": update_data}
        )
        mod_count = result.modified_count
        result = self.movies.find_one(result)
        if mod_count> 0:
            return mflix_pb2.PedidoResposta(
                filme=result,
                messagem=f"Filme {request.filme.id} alterado com sucesso \n {result}",
                sucesso=True
            )
        else:
            return mflix_pb2.Pedidoresposta(
                filme=result,
                mensagem=f"Nenhuma alteração foi realizada",
                sucesso=False
            )
    
    def delete_filme(self,request):
        if not request.filme.id:
            return mflix_pb2.PedidoResposta(
                mensagem="ID é obrigatório para a atualização",
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


    def doc_to_filme(self,doc):
        return mflix_pb2.Filme(
            id=str(doc.get("_id","")),
            titulo=doc.get("titulo",""),
            ano=doc.get("ano",0),
            duracao=doc.get("duracao",0),
            diretores=doc.get("diretores",[]),
            atores=doc.get("atores",[]),
            generos=doc.get("generos",[])
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mflix_pb2_grpc.add_FilmeServiceServicer_to_server(MovieServerRPC(), server)
    server.add_insecure_port("[::]:50051")
    print("Servidor iniciado na porta 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()