package org.example;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import org.example.grpc.FilmeServiceGrpc;
import org.example.grpc.FilmeServiceGrpc.FilmeServiceBlockingStub;
import org.example.grpc.FilmePedido;
import org.example.grpc.PedidoResposta;

public class GrpcCliente {

    private final ManagedChannel canal;
    private final FilmeServiceBlockingStub stub;

    // Construtor: cria o canal e o stub
    public GrpcCliente(String endereco, int porta) {
        this.canal = ManagedChannelBuilder
                .forAddress(endereco, porta)
                .usePlaintext() // sem TLS (modo dev)
                .build();

        this.stub = FilmeServiceGrpc.newBlockingStub(canal);
    }

    // Envia requisição e retorna resposta
    public PedidoResposta enviarPedido(FilmePedido pedido) {
        try {
            return stub.gerenciaFilmes(pedido);
        } catch (Exception e) {
            System.err.println("Erro ao chamar serviço gRPC: " + e.getMessage());
            return PedidoResposta.newBuilder()
                    .setMensagem("Falha na comunicação com o servidor")
                    .setSucesso(false)
                    .build();
        }
    }

    // Fecha o canal
    public void fechar() {
        if (canal != null && !canal.isShutdown()) {
            canal.shutdown();
        }
    }
}
