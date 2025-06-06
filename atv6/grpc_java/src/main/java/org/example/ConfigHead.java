package org.example;

import java.util.List;
import org.example.grpc.FilmePedido;
import org.example.grpc.Filme;
/*

 *Name: Guilherme Almeida Lopes
 *Name: Hugo Okumura

 *Create: 5-06-2025
 * Last modified: 5-06-2025
 */
// Class responsible for constructing and configuring gRPC requests
public class ConfigHead {

    // Default constructor
    ConfigHead() {
    }

    // Builds a POST request to create a new movie
    FilmePedido conf_post_filme(Filme body) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.reqType.POST);
        request.setFilme(body);
        return request.build();
    }

    // Builds a GET request to list movies by genre
    FilmePedido get_filme_gener(Filme body, List<String> list) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.reqType.GET);
        request.setFilme(body);
        request.addAllGeneros(list);
        return request.build();
    }

    // Builds a DELETE request to remove a movie by ID
    FilmePedido delete_filme(Filme body) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.reqType.DELETE);
        request.setFilme(body);
        return request.build();
    }

    // Builds an UPDATE request to modify an existing movie by ID
    FilmePedido update_filme_id(Filme body) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.reqType.UPDATE);  // CORRECTED
        request.setFilme(body);
        return request.build();
    }

    // Builds a GET request to search movies by actors
    FilmePedido get_filme_actor(Filme body, List<String> list) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.reqType.GET);  // CORRECTED
        request.setFilme(body);
        request.addAllAtores(list);
        return request.build();
    }

    // Builds a POST request to get a movie by ID (note: might need to be GET semantically)
    FilmePedido get_filme_id(Filme body) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.reqType.POST);
        request.setFilme(body);
        return request.build();
    }
}
