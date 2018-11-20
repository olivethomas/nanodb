# first of all import the socket library 
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

 
# next create a socket object
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      
except socket.error:
    print("Could not create socket. Error Code: ")
    sys.exit(0)
print ("Socket successfully created")

  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12345            
  
   
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
try:
    s.bind(('', port))
except:
    print ("Cannot bind to port")
    sys.exit()
    
print ("socket binded to %s" %(port)) 
  
# put the socket into listening mode 
s.listen(5)      
#print ('socket is listening')           

def client_thread(c):
    c.send(('Thank you for connecting').encode())
    while True:
        query=c.recv(1024).decode()
        if(query == "exit"):
            break
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
    c.close
    print("Client connection closed")

while True:
    c, addr = s.accept() 
    print ('Got connection from', addr)

    start_new_thread(client_thread, (c,))
s.close()

'''
# a forever loop until we interrupt it or  
# an error occurs 
while True: 
  
   # Establish connection with client. 
    c, addr = s.accept()      
    print ('Got connection from', addr) 
  
   # send a thank you message to the client.  
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
  
   # Close the connection with the client 
    c.close()
    break '''
