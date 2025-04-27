import hashlib
import sys
from User import *
import socket as sc
from SocketCliente  import SocketClient

def exit(socket, user):
    socket.send(f"EXIT {user}".encode())
    print("Disconnecting...")
    socket.close()


def configsocketclient():
    print("Initializing Client...")
    socketclient=SocketClient()
    hostname:str=sc.gethostbyname(sc.gethostname())
    socketclient.connect(hostname, int(sys.argv[1]))

    socket=socketclient.socket
    print("Connected to server")
    path:str="/"
    user:str=None
    return socket,path,user

def sendcreateuser(socket):
    print("Username:",end="")
    username=input()
    print("Password:",end="")
    password=input()
    passha256=hashlib.sha256(password.encode()).hexdigest()
    socket.send(f"CREATEUSER {username} {passha256}".encode())
    print(socket.recv(1024).decode())

def msg_login():
    print("don't have user autenticated ")
    print("Please login first")

def main():
    socket, path, user = configsocketclient()
    while True:
        if user==None:
            print(f"$[{path}]:",end="")
        else:
            print(f"${user}[{path}]:",end="")
        command=input().split(" ")
        
        if command[0]=="EXIT":
            exit(socket, user)
            break
        elif command[0]=="CONNECT":
            if len(command)<=2:
                print("Invalid command")
                return 0
            passha256=hashlib.sha256(command[2].encode()).hexdigest()
            socket.send(f"CONNECT {command[1]} {passha256}".encode())
            print("Connecting...")
            auth=socket.recv(1024).decode().split(",")
            print(auth[0])
            if auth[0]=="ERROR":
                print("User not found")
                continue
            user=auth[1]
        elif command[0]=="CREATEUSER":
            sendcreateuser(socket)
        elif user==None:
            msg_login()
            continue
        elif command[0]=="PWD"and user!=None:
            socket.send("PWD".encode())
            print(socket.recv(1024).decode())
        elif command[0]=="CHDIR" and user!=None:
            socket.send(f"CHDIR {command[1]}".encode())
            print(socket.recv(1024).decode())
        else:
            print("Command not found")



if __name__=="__main__":
    main()