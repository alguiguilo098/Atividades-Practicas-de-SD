from User import *
import sys
import hashlib
import socket as sc
from SocketServerOwn import ServerSocket
import os 

def change_directory(conn, data, pathfilesys):
    if len(data) < 2:
        print("Invalid command CHDIR")
        return pathfilesys
    new_path = os.path.join(pathfilesys, data[1])
    is_dir = os.path.isdir(new_path)
    print(f"Checking path: {new_path}")
    print(f"Is directory: {is_dir}")
    if data[1]==".." and pathfilesys!="./FileSystemServer/..":
        args=pathfilesys.split("/")
        pathfile=pathfilesys.strip(args[-1])
        conn.send("SUCCESS CHDIR".encode())
        return pathfile
    elif os.path.exists(new_path) and is_dir:
        pathfilesys = new_path
        conn.send("SUCCESS CHDIR".encode())
    else:
        conn.send("ERROR: Directory not found".encode())
        print(f"Current path: {pathfilesys}")
    return pathfilesys

def connect(conn, data):
    try:
        user=User.get(User.name==data[1]) # busca do usuario no banco de dados

        if user.password==data[2] and user.name==data[1]:
            conn.send(f"SUCCESS,{user.name}".encode())
            print(f"User {user.name} connected")
            return user.name
        else:
            conn.send('ERROR'.encode())
            print(f"User {user.name} not connected")
            return None
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

    socketserver:ServerSocket=ServerSocket(hostname, int(sys.argv[1]),25)
    (conn,_)=socketserver.accept()

    print("Server started")
    return conn