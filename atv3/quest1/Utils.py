#Name: Guilherme Almeida Lopes
# Create: 24-04-2025 
# Last modified: 27-04-2025

# Description: This is Logic Service for the server. 
# It handles the connection with the client and the logic of the file system.

from User import * # Import the User class
import hashlib # For hashing passwords 
import socket as sc # For socket programming 
from SocketServerOwn import ServerSocket # Import the ServerSocket class
import os # For file and directory operations 


def send_string_list(sock, items):
    # Envia o número de itens
    sock.send(str(len(items)).encode('utf-8'))
    sock.recv(1024)
    # Envia cada item
    buffer=""
    for item in items:
        itembreak=item+"\n"
        buffer+=itembreak
    sock.send(buffer.encode('utf-8'))
def handle_getfiles(sock, current_dir):
    files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    send_string_list(sock, files)
    print("Files sent to client")

def handle_getdirs(sock, current_dir):
    dirs = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
    send_string_list(sock, dirs)

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
            # autentication user sucess
            conn.send(f"SUCCESS,{user.name}".encode())
            print(f"User {user.name} connected")
            return user.name
        else:
            # authentication user failed
            conn.send('ERROR'.encode())
            print(f"User {user.name} not connected")
            return None
    except User.DoesNotExist:
        # user not found
        print("User not found")
        conn.send("ERROR".encode())

def create_user(conn, data):
    # Transform the password to sha256
    passsha256=hashlib.sha256(data[1].encode()).hexdigest()
    # Create User with the name and password
    User.create(name=data[1], password=passsha256)
    print(f"User created {data[1]}")
    # Send the message to the client
    conn.send("User created".encode())

def configDB():
    db.connect()
    db.create_tables([User])
    print("Initializing Server...")

def configSocketClient(port:int,hostname:str):
    # Get the hostname of the machine 
    print(f"Hostname: {hostname}")

    # Create a socket server
    socketserver:ServerSocket=ServerSocket(hostname,port,25)
    (conn,_)=socketserver.accept()

    print("Server started")
    return conn # socket to communicate with the client