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

2. Instale o Python e o Virtualenv na sua máquina:

   - Para sistemas baseados em Fedora:
     ```bash
     sudo dnf install python3 python3-virtualenv
     ```

   - Para sistemas baseados em Ubuntu/Debian:
     ```bash
     sudo apt install python3 python3-virtualenv
     ```

3. Crie um ambiente virtual:
   ```bash
   virtualenv .venv
   ```

4. Ative o ambiente virtual:
   ```bash
   source .venv/bin/activate
   ```

---

## Execução dos Arquivos

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

