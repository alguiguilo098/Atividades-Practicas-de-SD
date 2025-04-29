# Name: Guilherme Almeida Lopes
# Name: Hugo Okumura

# Create: 24-04-2025 
# Last modified: 27-04-2025

# Description: This is the server code for the file system. It handles the connection with the client and the logic of the file system.
# It uses a database to store the users and their passwords. It also handles the file 
# system operations like creating users, changing directories, getting files and directories.

import hashlib # for password hashing
import sys # for command line arguments
from User import * # for user database 
import socket as sc # for socket programming
from SocketCliente  import SocketClient 

def exit(socket, user):
    # exit of program client
    socket.send(f"EXIT {user}".encode())
    print("Disconnecting...")
    socket.close()


def configsocketclient(port,hostname):
    # This function configures the socket client
    print("Initializing Client...")
    socketclient=SocketClient()
    socketclient.connect(hostname, port)

    socket=socketclient.socket
    print("Connected to server")
    path:str="/"
    user:str=None
    return socket,path,user

def sendcreateuser(socket):
    # send user to server 
    print("Username:",end="")
    username=input() # get name 
    print("Password:",end="")
    password=input() # get password
    passha256=hashlib.sha256(password.encode()).hexdigest() # hash password
    socket.send(f"CREATEUSER {username} {passha256}".encode()) # send user to server
    print(socket.recv(1024).decode()) # receive response from server

def msg_login():
    # This function is called when the user is not autenticated
    print("don't have user autenticated ")
    print("Please login first")
    print("To login, use the command CONNECT <username> <password>")

def main():
    socket, path, user = configsocketclient(int(sys.argv[1]),sys.argv[2]) # configure socket client
    while True:
        if user==None:
            print(f"$[{path}]:",end="") # prompt not with user
        else:
            print(f"${user}[{path}]:",end="") # prompt with user
        command=input().split(" ")
        if command[0]=="EXIT":
            exit(socket, user) #exit program
            break # exit loop
        elif command[0]=="CONNECT":
            if len(command)<=2:
                # invalid command 
                print("Invalid command")
                return 0
            passha256=hashlib.sha256(command[2].encode()).hexdigest() # hash password
            socket.send(f"CONNECT {command[1]} {passha256}".encode()) # send user to server
            print("Connecting...") 
            auth=socket.recv(1024).decode().split(",") # receive response from server
            print(auth[0])
            if auth[0]=="ERROR":
                # invalid user 
                print("User not found")
                continue
            user=auth[1] # user autenticated 
        elif command[0]=="CREATEUSER":
            sendcreateuser(socket) # send new user to servet
        elif user==None:
            msg_login() # if user is not autenticated
            continue
        elif command[0]=="PWD"and user!=None:
            socket.send("PWD".encode()) # show current password
            print(socket.recv(1024).decode())
        elif command[0]=="CHDIR" and user!=None:
            socket.send(f"CHDIR {command[1]}".encode()) # change directory 
            print(socket.recv(1024).decode())
        elif command[0]=="GETDIR"and user!=None:
            socket.send(f"GETDIR {path}".encode()) # get directories 
            numdirs=int(socket.recv(1024).decode()) # number of directories
            socket.send("OK".encode()) # send ok to server 
            print(f"Number of directories:{numdirs}\n") # print number of directories
            dirs=socket.recv(1024).decode()
            print(dirs)
        elif command[0]=="GETFILE" and user!=None:
            socket.send(f"GETFILE {path}".encode()) # send getfiles command to server 
            numfile=int(socket.recv(1024).decode()) # recive number of files
            socket.send("OK".encode()) # send ok to server
            print(f"Number of files:{numfile}\n")
            files=socket.recv(1024).decode() # recive name of directorys
            print(files)
        else:
            print("Command not found")



if __name__=="__main__":
    main()