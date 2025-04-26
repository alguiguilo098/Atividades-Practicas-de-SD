from User import *
import sys
import hashlib
import socket as sc
from SocketServerOwn import ServerSocket
import os 

userlogin={}

def connect(conn, data):
    try:
        user=User.get(User.name==data[1]) # busca do usuario no banco de dados

        if user.password==data[2] and user.name==data[1]:
            conn.send(f"SUCCESS,{user.name}".encode())
            print(f"User {user.name} connected")
            userlogin[user.name]=user
        else:
            conn.send('ERROR'.encode())
            print(f"User {user.name} not connected")
    except User.DoesNotExist:
        print("User not found")
        conn.send("ERROR".encode())

def create_user(conn, data):
    passsha256=hashlib.sha256(data[1].encode()).hexdigest()
    User.create(name=data[1], password=passsha256)
    print(f"User created {data[1]}")
    conn.send("User created".encode())

def configDB():
    db.connect()
    db.create_tables([User])
    
    print("Initializing Server...")

def configSocketClient():
    hostname:str=sc.gethostbyname(sc.gethostname())
    print(f"Hostname: {hostname}")

    socketserver:ServerSocket=ServerSocket(hostname, int(sys.argv[1]),int(sys.argv[2]))
    (conn,host)=socketserver.accept()

    print("Server started")
    return conn

if __name__=="__main__":

    pathfilesys=["../FileSystem/","/"]
    configDB()
    conn = configSocketClient()

    while True:
        data=conn.recv(1024).decode()

        if data!="PWD":
            print("Não pwd")
            data=data.split(" ")

        print(f"Received data: {data}")
        if data[0]=="EXIT":
            print(f"User {data[1]} disconnected".encode())
            userlogin.pop(data[1])
        elif data[0]=="CONNECT":
            connect(conn, data)
        elif data[0]=="CREATEUSER":
            create_user(conn, data)
        elif data[0]=="CHDIR":
            if len(data) < 2:
                print("Invalid command CHDIR")
                continue
            if os.path.exists(os.path.join(pathfilesys[-1], data[1])) and os.path.isdir(os.path.join(pathfilesys[-1], data[1])):
                pathfilesys.append(data[1])
                conn.send("SUCCESS CHDIR".encode())
            else:
                conn.send("ERROR: Directory not found".encode())
            print(f"Current path:")
        elif data[0]=="GETFILE":
            pass
        elif data[0]=="GETDIR":
            pass
        elif data=="PWD":
            pwd=pathfilesys[1::]
            conn.send(f"Current path: {pwd}".encode())
        