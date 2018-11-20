# Import socket module 
import socket  
import os
import sys
import json
import pickle
from struct import unpack
import pprint
 
def bytes_to_number(b):
    # if Python2.x
    # b = map(ord, b)
    res = 0
    for i in range(4):
        res += b[i] << (i*8)
    return res
  
# Create a socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
  
# Define the port on which you want to connect 
port = 12345                
  
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
#s.send()


          
# receive data from the server 
print (s.recv(1024).decode())
while 1:
    query=input()
    s.send(query.encode())
    if query=="exit":
        break
    signal = s.recv(4) # assuming that the size won't be bigger then 1GB
    signal = bytes_to_number(signal)

    if signal:
        bs = s.recv(8)
        (length,)=unpack('>Q',bs)
        ba = b''
        while len(ba) < length:
            to_read = length - len(ba)
            ba+=s.recv(4096 if to_read > 4096 else to_read)
        data = pickle.loads(ba)
        #assert len(b'\00') == 1
        s.sendall(b'\00')
        '''
        b = b''
        while 1:
            tmp = s.recv(1024)
            b += tmp
        print (b)
        #data = json.loads(b.decode('utf-8'))'''
        #print (data)
        pprint.pprint(dict(data))
    else:
        data = s.recv(1024).decode()
        print (data)
    """
    current_size = 0
    buffer ="b"
    while current_size < size:
        data = s.recv(1024).decode()
        if not data:
            break
        if len(data) + current_size > size:
            data = data[:size-current_size] # trim additional data
        buffer += data
            # you can stream here to disk
        current_size += len(data)
        print (data)
        """
    # close the connection 
s.close()
s
