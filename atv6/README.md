# Mflix Software

O **Mflix Software** é um sistema distribuído composto por um **servidor grpc em Python** e um **cliente em Java**. Juntos, eles realizam operações **CRUD** sobre um banco de dados de filmes utilizando o **MongoDB**.

A comunicação entre cliente e servidor é feita de forma eficiente por meio do **Protocol Buffers (Protobuf)**, garantindo **velocidade**, **portabilidade** e **baixo consumo de rede**.

---

## 🎯 Objetivo

Este projeto tem como principal objetivo demonstrar o uso do **grpc** como meio de comunicação entre cliente e servidor. O grpc, por ser um protocolo binário, permite:

* Modularidade no desenvolvimento (cliente e servidor podem ser desenvolvidos separadamente);
* Melhor produtividade e escalabilidade.

---

## ⚙️ Configuração do Ambiente

### ✅ Pré-requisitos

* Python 3.x
* Java JDK 11 ou superior
* MongoDB (preferencialmente com MongoDB Atlas)
* [Protocol Buffers Compiler (`protoc`)](https://protobuf.dev/)
* `pip` (Python Package Installer)
* `mvn` (Maven para o cliente Java)

---

## 🖥️ Configuração do Servidor (Python)

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/alguiguilo098/Atividades-Practicas-de-SD.git
   cd Atividades-Practicas-de-SD/atv6/
   ```

2. **Instale o compilador do Protobuf:**

   ```bash
   sudo apt install protobuf-compiler
   ```

3. **Acesse o diretório do servidor e crie o ambiente virtual:**

   ```bash
   cd grpc_python/
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Instale as dependências do Python:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure o MongoDB Atlas:**

   5.1 Acesse [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) e crie uma conta.
   5.2 Crie um banco de dados e uma coleção.
   5.3 Escolha a linguagem "Python" para integração.
   5.4 Utilize o modelo `movies` e nomeie o banco como `mflix`.
   5.5 Copie a **string de conexão** da aba `Connect > Connect your application`.

6. **Atualize a string de conexão no código do servidor (linha 4 do `server.py`) com a sua URL do MongoDB Atlas.**

7. **Inicie o servidor:**

   ```bash
   python server.py
   ```

---

## 🧑‍💻 Configuração do Cliente (Java)

1. **Acesse o diretório do cliente:**

   ```bash
   cd ../grpc_java/
   ```

2. **Compile os arquivos `.proto`:**

   Certifique-se de que o arquivo `.proto` está na raiz ou no diretório `src/main/proto`. Depois, compile com:

   ```bash
   mvn compile
   ```

3. **Execute o cliente:**

   ```bash
   mvn exec:java
   ```

---

## 📁 Estrutura Geral do Projeto

```
Atividades-Practicas-de-SD/
├── atv6/
│   ├── grpc_python/         # Código do servidor Python
│   │   ├── server.py
│   │   ├── requirements.txt
│   │   └── venv/         # Ambiente virtual
│   └── grpc_java/       # Código do cliente Java
│       ├── pom.xml
│       └── src/
└── README.md             # (Este arquivo)
```

