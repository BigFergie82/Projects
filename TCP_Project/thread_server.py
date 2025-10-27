"""
Server side: open a socket on a port, listen for a message from a client,
and send an echo reply; echoes lines until eof when client closes socket;
spawns a thread to handle each client connection; threads share global
memory space with main thread; this is more portable than fork: threads
work on standard Windows systems, but process forks do not;
"""

import time, _thread as thread           # or use threading.Thread().start()
from socket import *                     # get socket constructor and constants
import re                                  # used to handle ?

myHost = ''                              # server machine, '' means local host
myPort = 50007                           # listen on a non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)           # make a TCP socket object
sockobj.bind((myHost, myPort))                   # bind it to server port number
sockobj.listen(5)                                # allow up to 5 pending connects

def now():
    return time.ctime(time.time())               # current time on the server

def handleClient(connection, address):          #connect to client at address
    print(f"Client {address} connected at {now()}")         #print the client's address and time of connection
    try:
        with open('wordlist.txt') as f:                     #same as before, used to open the text file and split by word
            words = [w.strip() for w in f.readlines()]

        while True:                                 #same as before, except now it is in a while loop to allow for multiple connections
            data = connection.recv(1024)
            if not data:
                connection.close()


            query = data.decode().strip()                   #decodes the query from string to bytes

            if query.lower() == "quit":         #if the query is quit then it ends the connection
                connection.close()


            regex = '^' + query.replace('?', '.') + '$'         #same as before for finding matches, used w3schools for example code and understanding how regex works
            matches = [w for w in words if re.match(regex, w)]

            if matches:
                header = f"200 OK {len(matches)}\n"             #same as before, combines the header code with the number of matches
                body = "\n".join(matches) + "\n"                #inputs all the matches into a list separated by lines
                connection.sendall((header + body).encode())        #combines all and sends to client
            else:
                connection.send(b"404 NOT FOUND\n")         #if no matches found return 404

    except Exception as e:                  #same as before, if there is any errors, print it
        print(e)

def dispatcher():                                # listen until process killed
    while True:                                  # wait for next connection,
        connection, address = sockobj.accept()   # pass to thread for service
        print('Server connected by', address, end=' ') 
        print('at', now())
        thread.start_new_thread(handleClient, (connection, address))

dispatcher()


