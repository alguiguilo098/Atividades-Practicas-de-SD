package org.example;
import org.example.grpc.PedidoResposta;
import org.example.grpc.Filme;
import java.util.List;

public class TablesMovies {

    private static  void print_table(List<Filme> listmovie){
        for(Filme movie:listmovie){
            System.out.println(movie.toString());
        }
    }
    static void show_movie(PedidoResposta pedido){
        TablesMovies.print_table(pedido.getFilmesList());
    }

}
