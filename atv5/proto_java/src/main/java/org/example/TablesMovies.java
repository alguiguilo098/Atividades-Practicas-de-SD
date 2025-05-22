package org.example;
import mflix.Mflix.PedidoResposta;
import mflix.Mflix.Filme;
import java.util.List;

public class TablesMovies {

    static private void print_table(List<Filme> listmovie){
        for(Filme movie:listmovie){
            System.out.println(movie.toString());
        }
    }
    static void show_movie(PedidoResposta pedido){
            List<Filme>lista=pedido.getFilmesList();
            TablesMovies.print_table(lista);
    }

}
