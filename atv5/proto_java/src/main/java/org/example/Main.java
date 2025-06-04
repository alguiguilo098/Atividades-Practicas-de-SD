package org.example;
/*
    *Name: Guilherme Almeida Lopes
    *Name: Hugo Okumura
    *Create: 16-05-2025
    * Last modified: 21-05-2025

    *This Java code defines the entry point (main method) for the client application.
    *It prompts the user to input the server IP address and port number, establishes a socket connection using this information,
    * and then starts the interactive movie client menu*
 */
import java.util.Scanner;
public class Main{
    public static void main(String[] args) {
    try {
        Scanner sca=new Scanner(System.in);
        System.out.println("IP da Rede:");
        String ip= sca.next();
        System.out.println("Port:");
        int port= sca.nextInt();
        System.out.println();
        SocketCliente socketcliente=new SocketCliente(ip,port);
        MenuCliente menu=new MenuCliente(socketcliente);
        menu.run();

    } catch (Exception e) {
        System.out.println(e.getMessage());
    }
}
}