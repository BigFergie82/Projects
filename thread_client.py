from socket import *        #import socket elements

HOST = ''         #same as server, blank for local host
PORT = 50007      #same as server

sockobj = socket(AF_INET, SOCK_STREAM)          #create a TCP socket
sockobj.connect((HOST, PORT))   #connect the socket to the server at the given host and port

while True:                                     #now under a loop which allows multiple inputs
    query = input("Enter query: ")       #same as before, enter query
    sockobj.sendall(query.encode())     #same, send query to server

    if query.lower() == "quit":               #if the query is quit, break the connection
        break                       

    response = sockobj.recv(4096).decode()      #decode the servers response
    print(response)         #print

sockobj.close()         #close the connection after the while loop is finished