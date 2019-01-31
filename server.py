import socket 
import os
from collections import OrderedDict
from storage import Storage
from query import Query
import sys
import json
import pickle
from struct import pack
from _thread import start_new_thread


def convert_to_bytes(no):
    result = bytearray()
    result.append(no & 255)
    for i in range(3):
        no = no >> 8
        result.append(no & 255)
    return result

 
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      
except socket.error:
    print("Could not create socket. Error Code: ")
    sys.exit(0)
print ("Socket successfully created")

port = 12345            
  
try:
    s.bind(('', port))
except:
    print ("Cannot bind to port")
    sys.exit()
    
print ("socket binded to %s" %(port)) 
  
s.listen(5)      
#print ('socket is listening')           

def client_thread(c):
    c.send(('Thank you for connecting').encode())
    while 1:                                                            #outer loop
        while 1:                                                        #loop for login and register.breaks on exit or successful login 
            command=c.recv(1024).decode()
            if command=="exit":
                break
            if command=="login" or command=="register":
                username=c.recv(1024).decode()
                password=c.recv(1024).decode()
                queryobj = Query()
                if command=="login":
                    retval=queryobj._login(username,password)
                        
                else:
                    retval=queryobj._register(username,password)
            else:
                retval="Invalid command"
            c.send(retval.encode())
            if retval=="Successfully logged in":
                break
        if command=="exit":                                             #condition to exit
            break
        
        while True:                                                     #query loop
            query=c.recv(1024).decode()
            #queryobj = Query()
            if(query == "logout" or query=="exit"):                                     #user logout
                queryobj._logout()
                break
            result = queryobj.match(query)
            
            if isinstance(result,str):
                c.send(convert_to_bytes(0)) 
                c.send(result.encode())
            else:
                c.send(convert_to_bytes(1))
                #buff = json.dumps(result).encode('utf-8')
                #print (buff)
                #c.sendall(buff)
                data = pickle.dumps(result)
                length = pack('>Q',len(data))
                c.sendall(length)
                c.sendall(data)

                ack = c.recv(1)
        c.close
        print("Client connection closed")
        if query=="exit":
            break
while True:
    c, addr = s.accept() 
    print ('Got connection from', addr)

    start_new_thread(client_thread, (c,))
s.close()
''' 
    while True: 
       
        c, addr = s.accept()      
        print ('Got connection from', addr) 
        c.send(('Thank you for connecting').encode()) 

        while 1:
            query=c.recv(1024).decode()
            queryobj = Query()
            result = queryobj.match(query)
            
            if isinstance(result,str):
                c.send(convert_to_bytes(0)) 
                c.send(result.encode())
            else:
                c.send(convert_to_bytes(1))
                #buff = json.dumps(result).encode('utf-8')
                #print (buff)
                #c.sendall(buff)
                data = pickle.dumps(result)
                length = pack('>Q',len(data))
                c.sendall(length)
                c.sendall(data)

                ack = c.recv(1)
            """
                    d = infile.read(1024)
            while d:
                        c.send(d.encode())
                        d = infile.read(1024)
            """
      
        c.close()
        break '''
