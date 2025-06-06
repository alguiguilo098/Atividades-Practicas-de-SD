/*

 *Name: Guilherme Almeida Lopes
 *Name: Hugo Okumura

 *Create: 5-06-2025
* Last modified: 5-06-2025

 * This Java code implements a terminal-based client that interacts with a movie server grpc  to
 * send and receive movie information.
 */
package org.example;
import java.util.List;
import java.util.Scanner;
import org.example.grpc.FilmePedido;
import org.example.grpc.Filme;
import org.example.grpc.PedidoResposta;

class MenuCliente {

    // Main attributes: gRPC socket, scanner for user input, and request configuration handler
    private GrpcCliente socket;
    private Scanner sca;
    private ConfigHead operations;

    // Constructor: initializes components and displays connection messages
    MenuCliente(GrpcCliente socketcliente){
        System.out.println("Initializing Client ...");
        System.out.println("Establishing Connections");
        this.socket = socketcliente;
        System.out.println("Connection established with server");
        this.sca = new Scanner(System.in);
        this.operations = new ConfigHead();
    }

    // Displays the main menu options
    private void show_menu(){
        System.out.println("1- Create Movie");
        System.out.println("2- Delete Movie");
        System.out.println("3- Update Movie");
        System.out.println("4- List by genres");
        System.out.println("5- List by actors");
        System.out.println("6- Exit");
    }

    // Prompts user to input movie data and returns a Filme.Builder object
    private Filme.Builder criar_filme(){
        System.out.print("Title: ");
        String titulo = sca.next();
        System.out.print("Directors: ");
        String diretores = sca.next();
        System.out.print("Year: ");
        int ano = sca.nextInt();
        System.out.print("Actors: ");
        String atores = sca.next();
        System.out.print("Duration: ");
        int duracao = sca.nextInt();
        System.out.print("Genre: ");
        String genero = sca.next();
        return constructormovie(titulo, ano, duracao, diretores, atores, genero);
    }

    // Constructs a Filme.Builder using the provided movie data
    private static Filme.Builder constructormovie(String titulo, int ano, int duracao, String diretores, String atores, String genero) {
        Filme.Builder movie = Filme.newBuilder().setTitulo(titulo).setAno(ano).setDuracao(duracao);
        movie.addAllDiretores(List.of(diretores.split(",")));
        movie.addAllAtores(List.of(atores.split(",")));
        movie.addAllGeneros(List.of(atores.split(","))); // WARNING: using 'atores' instead of 'genero'
        return movie;
    }

    // Handles the selected menu option
    private void choice(int options){
        if (options == 1) {
            postmovie();
        } else if (options == 2) {
            delete_filme();
        } else if (options == 3) {
            update_filme();
        } else if (options == 4) {
            getgenermovie();
        } else if (options == 5) {
            get_actors_movie();
        } else if (options == 6) {
            System.exit(-1);
        } else {
            System.out.println("ERROR: Invalid option!");
        }
    }

    // Sends a request to create a movie
    private void postmovie() {
        Filme filme = criar_filme().build();
        FilmePedido pedido = this.operations.conf_post_filme(filme);
        System.out.println("Sending request ...");

        System.out.println("Waiting for response ...");
        PedidoResposta response = socket.enviarPedido(pedido);

        System.out.println(response.getMensagem());
    }

    // Sends a request to fetch a movie by ID (not currently used in menu)
    private void getfilme() {
        System.out.print("Id: ");
        String id = sca.next();
        Filme filme = Filme.newBuilder().setId(id).build();
        FilmePedido pedido = this.operations.get_filme_id(filme);
        System.out.println("Sending request ...");
        System.out.println("Waiting for response ...");
        PedidoResposta response = socket.enviarPedido(pedido);
    }

    // Sends a request to delete a movie by ID
    private void delete_filme() {
        System.out.print("Id: ");
        String id = sca.next();
        Filme filme = Filme.newBuilder().setId(id).build();
        FilmePedido pedido = this.operations.delete_filme(filme);

        System.out.println("Sending request ...");
        System.out.println("Waiting for response ...");
        PedidoResposta response = socket.enviarPedido(pedido);

        System.out.println(response.getMensagem());
    }

    // Sends a request to list movies by actors
    private void get_actors_movie(){
        System.out.print("Actors: ");
        String actors = sca.next();
        List<String> listactor = List.of(actors.split(","));
        Filme filme = Filme.newBuilder().build();
        FilmePedido pedido = this.operations.get_filme_actor(filme, listactor);
        PedidoResposta response = socket.enviarPedido(pedido);
        if (response.getSucesso()) {
            TablesMovies.show_movie(response);
        } else {
            System.out.println(response.getMensagem());
        }
    }

    // Sends a request to list movies by genres
    private void getgenermovie(){
        System.out.print("Genres: ");
        String gener = sca.next();
        List<String> listgener = List.of(gener.split(","));
        Filme filme = Filme.newBuilder().build();
        FilmePedido pedido = this.operations.get_filme_gener(filme, listgener);
        PedidoResposta response = socket.enviarPedido(pedido);
        if (response.getSucesso()) {
            TablesMovies.show_movie(response);
        } else {
            System.out.println(response.getMensagem());
        }
    }

    // Sends a request to update a movie using its ID
    private void update_filme(){
        System.out.print("Id: ");
        String id = sca.next(); // movie ID
        Filme movie = criar_filme().setId(id).build(); // build movie with ID
        FilmePedido pedido = this.operations.update_filme_id(movie);

        PedidoResposta response = socket.enviarPedido(pedido);
        System.out.println(response.getMensagem());
    }

    // Main loop: runs the menu continuously and processes user choices
    public void run(){
        while (true){
            show_menu();
            System.out.print("Input: ");
            int options = sca.nextInt();
            this.choice(options);
        }
    }
}


