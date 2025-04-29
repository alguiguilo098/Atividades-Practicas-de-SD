Claro! Aqui está a versão limpa do `README.md`, sem os ícones e com formatação adequada para uso em projetos:

---

# Atividade 1 – Programação com Sockets TCP  
**Disciplina:** Sistemas Distribuídos  
**Professor:** Rodrigo Campiolo  

## Objetivo

Esta atividade tem como objetivo desenvolver a habilidade de programação em redes utilizando **Sockets TCP**, com foco na criação de **servidores multiclientes**, comunicação baseada em comandos e manipulação remota de arquivos e diretórios.

---

## Configuração do Ambiente

1. Clone o repositório:
   ```bash
   git clone "<URL>"
   ```
2. Acesse o diretório do projeto:
   ```bash
   cd <diretório_do_projeto>
   ```
3. Instale o Python e o Virtualenv na sua máquina:

   - Para sistemas baseados em Fedora:
     ```bash
     sudo dnf install python3 python3-virtualenv
     ```

   - Para sistemas baseados em Ubuntu/Debian:
     ```bash
     sudo apt install python3 python3-virtualenv
     ```

4. Crie um ambiente virtual:
   ```bash
   virtualenv .venv
   ```

5. Ative o ambiente virtual:
   ```bash
   source .venv/bin/activate
   ```
6. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
---

## Execução dos Arquivos Questão 1
   Para executar os arquivos da questão 1, utilize o seguintes comandos:
   ```bash
      cd quest1
   ```
### Server.py
   Para rodar o servidor, utilize o seguinte comando:
   ```bash
      python3 Server.py <ip_do_servidor> <quantidade_de_clientes> <porta1> ...<portaN>
   ```
### Cliente.py

   Para rodar o cliente, utilize o seguinte comando:
   ```bash
      python3 Client.py <ip_do_servidor> <porta>
   ```
### Operações 
   O cliente pode executar as seguintes operações:
   - CREATEUSER: Cria um novo usuário.
   - CONNECT <user> <password>: Autentica um usuário existente
   - PWD: Mostra o diretório atual que o cliente está no servidor 
   - CHDIR <diretório> ou .. : Muda o diretório atual do cliente no servidor
   - GETFILE: Mostra a quantide de arquivo do diretório atual 
   - GETDIR: Mostra a quantidade de diretórios do diretório atual

### EXEMPLO DE USO
   ```
      bash
       
      CREATEUSER 
      # informe o nome do usuário e a senha (exemplo: ddd, ddd)

      CONNECT ddd ddd
      # informe o nome do usuário e a senha (exemplo: ddd,ddd)

      PWD
      # Mostra o diretório atual do cliente no servidor

      CHDIR Bleach 
      # Muda o diretório atual do cliente no servidor para o diretório Bleach

      GETFILE
      # Mostra a quantidade de arquivos do diretório atual do cliente no servidor 

      CHDIR ..
      # Muda o diretório atual do cliente no servidor para o diretório anterior

      GETDIR
      # Mostra a quantidade de diretórios do diretório atual do cliente no servidor

   ```
---

## Execução dos Arquivos Questão 2

### FileServer.py

Servidor responsável por gerenciar múltiplos clientes e armazenar arquivos enviados.

**Como executar:**
```bash
python3 FileServer.py
```

---

### FileClient.py

Cliente responsável por se conectar ao servidor e executar comandos remotamente.

**Como executar:**
```bash
python3 FileClient.py
```

---

## Exemplo de Uso

1. Em um terminal, execute o servidor:
   ```bash
   python3 FileServer.py
   ```

2. Em outro terminal, execute o cliente:
   ```bash
   python3 FileClient.py
   ```

3. No diretório criado automaticamente pelo cliente, crie um arquivo de teste.

4. No terminal do cliente, envie o arquivo usando:
   ```bash
   1 nomedoarquivo.extensao
   ```
   ou
   ```bash
   ADDFILE nomedoarquivo.extensao
   ```

5. Verifique as mensagens de resposta do servidor.

6. Para encerrar o cliente, digite:
   ```bash
   5
   ```
   ou
   ```bash
   SAIR
   ```

---

## Bibliotecas Utilizadas

- os  
- socket  
- logging  
- struct  
- peewee  

