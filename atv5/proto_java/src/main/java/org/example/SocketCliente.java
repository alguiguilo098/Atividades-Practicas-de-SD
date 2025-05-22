package org.example;

/*
 * Name: Guilherme Almeida Lopes
 * Name: Hugo Okumura
 *
 * Created: 16-05-2025
 * Last modified: 21-05-2025
 *
 * This class handles TCP communication between the Java client and a movie server.
 * It sends and receives Protocol Buffers messages over a socket.
 */

import java.net.*;
import java.io.*;
import java.nio.ByteBuffer;

import mflix.Mflix.PedidoResposta;
import mflix.Mflix.FilmePedido;

public class SocketCliente {

    private Socket cliente;
    private OutputStream out;
    private DataInputStream in;

    // Constructor - connects to the given address and port
    public SocketCliente(String endereco, int porta) {
        try {
            System.out.println("Setting up socket...");
            this.cliente = new Socket(endereco, porta);  // connects immediately
            System.out.println("Socket connected");

            // Get output and input streams from the socket
            this.out = cliente.getOutputStream();
            this.in = new DataInputStream(cliente.getInputStream());

        } catch (UnknownHostException e) {
            System.err.println("Unknown address: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("I/O error: " + e.getMessage());
            System.exit(-1);
        }
    }

    // Sends a FilmePedido request to the server
    public void sendFilmeRequest(FilmePedido request) {
        try {
            byte[] requestBytes = request.toByteArray();
            int size = requestBytes.length;

            // Send the size of the message as 4 bytes (big endian)
            byte[] sizeBytes = ByteBuffer.allocate(4).putInt(size).array();
            out.write(sizeBytes);

            // Send the actual data
            out.write(requestBytes);
            out.flush();

        } catch (IOException e) {
            System.err.println("Error sending data: " + e.getMessage());
        }
    }

    // Receives a PedidoResposta response from the server
    public PedidoResposta receiveFilmeResponse() {
        try {
            // Lê os 4 bytes do tamanho
            byte[] sizeBytes = new byte[4];
            in.readFully(sizeBytes);

            // Converte para int
            int size = ((sizeBytes[0] & 0xFF) << 24) |
                    ((sizeBytes[1] & 0xFF) << 16) |
                    ((sizeBytes[2] & 0xFF) << 8)  |
                    (sizeBytes[3] & 0xFF);

            // Lê os bytes da mensagem
            byte[] buffer = new byte[size];
            in.readFully(buffer);

            // Parse com Protobuf
            return PedidoResposta.parseFrom(buffer);
        } catch (IOException e) {
            System.err.println("Error receiving response: " + e.getMessage());
            return null;
        }
    }

    // Closes the socket and releases resources
    public void fechar() {
        try {
            if (cliente != null) cliente.close();
        } catch (IOException e) {
            System.err.println("Error closing socket: " + e.getMessage());
        }
    }
}
