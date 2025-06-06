package org.example;

import java.util.List;
import java.util.Scanner;
import org.example.grpc.FilmePedido;
import org.example.grpc.Filme;
import org.example.grpc.PedidoResposta;

import java.util.List;

public class ConfigHead {

    ConfigHead() {
    }

    FilmePedido conf_post_filme(Filme body) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.reqType.POST);  // CORRIGIDO
        request.setFilme(body);
        return request.build();
    }

    FilmePedido get_filme_gener(Filme body, List<String> list) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.reqType.GET);  // CORRIGIDO
        request.setFilme(body);
        request.addAllGeneros(list);
        return request.build();
    }

    FilmePedido delete_filme(Filme body) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.reqType.DELETE);  // CORRIGIDO
        request.setFilme(body);
        return request.build();
    }

    FilmePedido update_filme_id(Filme body) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.reqType.UPDATE);  // CORRIGIDO
        request.setFilme(body);
        return request.build();
    }

    FilmePedido get_filme_actor(Filme body, List<String> list) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.reqType.GET);  // CORRIGIDO
        request.setFilme(body);
        request.addAllAtores(list);
        return request.build();
    }

    FilmePedido get_filme_id(Filme body) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.reqType.POST);  // ATENÇÃO: talvez deva ser GET
        request.setFilme(body);
        return request.build();
    }
}
