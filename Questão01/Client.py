import hashlib
import sys
import socket as sc
from SocketCliente  import SocketClient

if __name__=="__main__":
    print("Initializing Client...")
    socketclient=SocketClient()
    hostname:str=sc.gethostbyname(sc.gethostname())
    socketclient.connect(hostname, int(sys.argv[1]))
    socket=socketclient.socket
    print("Connected to server")
    path:str="/"
    while True:
        print(f"$[{path}]:",end="")
        command=input().split(" ")
        
        if command[0]=="EXIT":
            break
        elif command[0]=="CONNECT":
            if len(command)<=2:
                print("Invalid command")
                continue
            passha256=hashlib.sha256(command[2].encode()).hexdigest()
            socket.send(f"CONNECT {command[1]} {passha256}".encode())
            print("Connecting...")
            print(socket.recv(1024).decode())

        elif command[0]=="CREATEUSER":
            print("Username:",end="")
            username=input()
            print("Password:",end="")
            password=input()
            passha256=hashlib.sha256(password.encode()).hexdigest()
            socket.send(f"CREATEUSER {username} {passha256}".encode())
            print(socket.recv(1024).decode())
        elif command[0]=="PWD":
            socket.send("PWD".encode())
            print(socket.recv(1024).decode())
        else:
            print("Command not found")
