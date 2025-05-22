package org.example;

import mflix.Mflix.FilmePedido;
import mflix.Mflix.Filme;

import java.util.List;

/*
 * Name: Guilherme Almeida Lopes
 * Name: Hugo Okumura
 *
 * Created: 16-05-2025
 * Last modified: 21-05-2025
 *
 * The ConfigHead class serves as a helper utility for constructing different types
 * of FilmePedido requests using Protocol Buffers.
 * These requests are sent from the client to the server to perform movie-related operations.
 */
public class ConfigHead {

    // Default constructor
    ConfigHead() {
    }

    // Constructs a POST request with a movie object to add a new movie
    FilmePedido conf_post_filme(Filme body) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.ReqType.POST);
        request.setFilme(body);
        return request.build();
    }

    // Constructs a GET request to search for movies by genre
    FilmePedido get_filme_gener(Filme body, List<String> list) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.ReqType.GET);
        request.setFilme(body);
        request.addAllGeneros(list);
        return request.build();
    }

    // Constructs a DELETE request to remove a movie
    FilmePedido delete_filme(Filme body) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.ReqType.DELETE);
        request.setFilme(body);
        return request.build();
    }

    // Constructs an UPDATE request to update a movie by its ID
    FilmePedido update_filme_id(Filme body) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.ReqType.UPDATE);
        request.setFilme(body);
        return request.build();
    }

    // Constructs a GET request to search for movies by actors
    FilmePedido get_filme_actor(Filme body, List<String> list) {
        FilmePedido.Builder request = FilmePedido.newBuilder();
        request.setTipoRequisicao(FilmePedido.ReqType.GET);
        request.setFilme(body);
        request.addAllAtores(list);
        return request.build();
    }

}
