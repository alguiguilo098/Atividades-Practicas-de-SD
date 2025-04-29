# Name: Guilherme Almeida Lopes
# Name: Hugo Okumura

# Create: 24-04-2025 
# Last modified: 27-04-2025

# Description: This is the Client code for the file system. 
# It handles the connection with thre server and the logic of the file system.

from Utils import * # Implemetation logic for the server
import threading # for threading
import sys # system arguments
def LogicService(port:int):
    pathfilesys="./FileSystemServer/"
    configDB()
    conn = configSocketClient(port,sys.argv[1])
    user=None
    while True:
        data=conn.recv(1024).decode() # Receive data from the client

        if data!="PWD":
            # PWD is a special case, don't split  data
            print("Não pwd")
            data=data.split(" ")

        print(f"Received data: {data}")
        if data[0]=="EXIT":
            # Disconnect the user
            print(f"User {data[1]} disconnected")
            sys.exit(0) #kill the thread
        elif data[0]=="CONNECT":
            # Connect to the server
            user=connect(conn, data)
        elif data[0]=="CREATEUSER":
            #Create a new user 
            create_user(conn, data)
        elif data[0]=="CHDIR" and user!=None:
            # Change to new directory
            pathfilesys=change_directory(conn, data, pathfilesys)
            print(pathfilesys)
        elif data[0]=="GETFILE" and user!=None:
            # Get the list of files
            handle_getfiles(conn, pathfilesys)
        elif data[0]=="GETDIR"and user!=None:
            # Get the list of directories
            handle_getdirs(conn,pathfilesys)
        elif data=="PWD"and user!=None:
            # Show the current path
            pwd=pathfilesys[18::]
            conn.send(f"Current path:{pwd}".encode())
        else:
            # Invalid command
            print("Invalid command")


if __name__=="__main__":
    threads=[] # list of threads
    pos=3 #position of the first port
    
    for i in range(int(sys.argv[2])):
        # Create a thread for each port
        threads.append(threading.Thread(target=LogicService,args=(int(sys.argv[pos]),)))
        pos+=1

    # Start all threads
    for th in threads:
        th.start()
    # main thread wait for all threads to finish 
    for th in threads:
        th.join()
