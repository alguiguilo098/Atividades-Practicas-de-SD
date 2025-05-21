/*

*Name: Guilherme Almeida Lopes
*Name: Hugo Okumura

*Create: 16-05-2025
* Last modified: 21-05-2025

* This Java code implements a terminal-based client that interacts with a movie server (via TCP socket) using Protocol Buffers to
* send and receive movie information.
*/
package org.example;
import java.util.List;
import java.util.Scanner;
import  mflix.Mflix.*;

class MenuCliente {

    private SocketCliente socket;
    private Scanner sca;
    private ConfigHead operations;

    MenuCliente(SocketCliente socketcliente){
        System.out.println("Incializando Cliente ...");
        System.out.println("Incializando Conexeções");
        this.socket=socketcliente;
        System.out.println("Conexão estabelecida com servidor");
        this.sca=new Scanner(System.in);
        this.operations= new ConfigHead();
    }
    private void show_menu(){
        System.out.println("1- Criar Filme ");
        System.out.println("2- Pegar Filme por id");
        System.out.println("3- Deletar Filme");
        System.out.println("4- Atualizar Filme");
        System.out.println("5- Listar por gênero");
        System.out.println("6- Listar por agores");
    }
    private Filme.Builder criar_filme(){
        System.out.print("Titulo: ");
        String titulo=sca.next();
        System.out.print("Diretores: ");
        String diretores= sca.next();
        System.out.print("Ano: ");
        int ano=sca.nextInt();
        System.out.print("Atores: ");
        String atores=sca.next();
        System.out.print("Duração: ");
        int duracao=sca.nextInt();
        System.out.print("Genero: ");
        String genero=sca.next();
        return constructormovie(titulo, ano, duracao,
                diretores, atores,genero);
    }
    private static Filme.Builder constructormovie(String titulo, int ano, int duracao, String diretores, String atores,String genero) {
        Filme.Builder movie=Filme.newBuilder().setTitulo(titulo).setAno(ano).setDuracao(duracao);
        movie.addAllDiretores(List.of(diretores.split(",")));
        movie.addAllAtores(List.of(atores.split(",")));
        movie.addAllGeneros(List.of(atores.split(",")));
        return movie;
    }

    private void choice(int options){
        if (options == 1) {
            postmovie();
        }else if (options==2){
            getfilme();
        }else if (options==3){
            delete_filme();
        } else if (options==4) {
            update_filme();
        } else if (options==6) {
        }else if(options==5){
            getgenermovie();
        }else{
            System.out.println("ERROR Information !!!");
        }
    }

    private void postmovie() {
        Filme filme=criar_filme().build();
        FilmePedido pedido =this.operations.conf_post_filme(filme);
        System.out.println("Enviado Requisição ...");
        socket.sendFilmeRequest(pedido);
        System.out.println("Enviado Recebendo Resposta ...");
        PedidoResposta response=socket.receiveFilmeResponse();

        System.out.println(response);
    }

    private void getfilme() {
        System.out.print("Id: ");
        String id=sca.next();
        Filme filme=Filme.newBuilder().setId(id).build();
        FilmePedido pedido =this.operations.get_filme_id(filme);
        socket.sendFilmeRequest(pedido);

        PedidoResposta response=socket.receiveFilmeResponse();
    }

    private void delete_filme() {
        System.out.print("Id: ");
        String id=sca.next();
        Filme filme=Filme.newBuilder().setId(id).build();
        FilmePedido pedido =this.operations.delete_filme(filme);
        socket.sendFilmeRequest(pedido);
        socket.receiveFilmeResponse();

        PedidoResposta response=socket.receiveFilmeResponse();
    }
    private void get_actors_movie(){
        System.out.print("actors:");
        String actors=sca.next();
        List<String>listactor=List.of(actors.split(","));
        Filme filme=Filme.newBuilder().build();
        FilmePedido pedido =this.operations.get_filme_actor(filme,listactor);
        socket.sendFilmeRequest(pedido);
        socket.receiveFilmeResponse();
    }
    private void getgenermovie(){
        System.out.print("geners:");
        String gener=sca.next();
        List<String>listgener=List.of(gener.split(","));
        Filme filme=Filme.newBuilder().build();
        FilmePedido pedido =this.operations.get_filme_gener(filme,listgener);
        socket.sendFilmeRequest(pedido);
        PedidoResposta calvo=socket.receiveFilmeResponse();


    }
    private void update_filme(){
        System.out.print("Id: ");
        String id=sca.next();
        Filme movie=criar_filme().setId(id).build();
        FilmePedido pedido =this.operations.update_filme_id(movie);
        socket.sendFilmeRequest(pedido);
        socket.receiveFilmeResponse();

    }
    public  void run(){
        while (true){
            show_menu();
            System.out.print("Input:");
            int options=sca.nextInt();
            this.choice(options);
        }
    }
}

