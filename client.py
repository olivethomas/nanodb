# Import socket module 
import socket  
import os
import sys

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

query=input()

s.send(query.encode())
size = s.recv(4) # assuming that the size won't be bigger then 1GB
size = bytes_to_number(size)
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
# close the connection 
s.close()