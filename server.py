# first of all import the socket library 
import socket 
import os
from collections import OrderedDict
from storage import storage 
import sys

def convert_to_bytes(no):
    result = bytearray()
    result.append(no & 255)
    for i in range(3):
        no = no >> 8
        result.append(no & 255)
    return result

 
# next create a socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          
print ("Socket successfully created")
  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12345                
  
   
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
s.bind(('', port))         
print ("socket binded to %s" %(port)) 
  
# put the socket into listening mode 
s.listen(5)      
#print ('socket is listening')           
  
# a forever loop until we interrupt it or  
# an error occurs 
while True: 
  
   # Establish connection with client. 
    c, addr = s.accept()      
    print ('Got connection from', addr) 
  
   # send a thank you message to the client.  
    c.send(('Thank you for connecting').encode()) 

    query=c.recv(1024).decode()
    tokens=query.split(" ")
    filename=tokens[-1]
    
    if os.path.exists(filename):
        length = os.path.getsize(filename)
        c.send(convert_to_bytes(length)) # has to be 4 bytes
        with open(filename, 'r') as infile:
            d = infile.read(1024)
            while d:
                c.send(d.encode())
                d = infile.read(1024)
    
  
   # Close the connection with the client 
    c.close()
    break