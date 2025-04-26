from User import *
import sys
import hashlib
import socket as sc
from SocketServerOwn import ServerSocket
import os 

def connect(conn, data):
    try:
        user=User.get(User.name==data[1]) # busca do usuario no banco de dados

        if user.password==data[2] and user.name==data[1]:
            conn.send("SUCCESS".encode())
            print(f"User {user.name} connected")
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

if __name__=="__main__":

    pathfilesys=["../FileSystem/","/"]

    db.connect()
    db.create_tables([User])
    
    user=None

    print("Initializing Server...")
    
    hostname:str=sc.gethostbyname(sc.gethostname())
    print(f"Hostname: {hostname}")

    socketserver:ServerSocket=ServerSocket(hostname, int(sys.argv[1]),int(sys.argv[2]))
    (conn,host)=socketserver.accept()

    print("Server started")

    while True:
        data=conn.recv(1024).decode()
        if data!="PWD":
            print("Não pwd")
            data=data.split(" ")

        print(f"Received data: {data}")
        if data[0]=="EXIT":
            print(f"User {data[1]} disconnected".encode())
        elif data[0]=="CONNECT":
            connect(conn, data)
        elif data[0]=="CREATEUSER":
            create_user(conn, data)
        elif data=="PWD":
            pwd=pathfilesys[1::]
            conn.send(f"Current path: {pwd}".encode())
        