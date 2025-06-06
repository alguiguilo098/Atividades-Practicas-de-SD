package org.example;

import org.example.grpc.PedidoResposta;
import org.example.grpc.Filme;
import java.util.List;

// Utility class to display movies in a table-like format
public class TablesMovies {

    // Private method to print each movie from the list
    private static void print_table(List<Filme> listmovie){
        for (Filme movie : listmovie) {
            System.out.println(movie.toString());
        }
    }

    // Public method to extract and display the list of movies from a response
    static void show_movie(PedidoResposta pedido){
        TablesMovies.print_table(pedido.getFilmesList());
    }
}
