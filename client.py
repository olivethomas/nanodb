import socket  
import os
import sys
import json
import pickle
import getpass
from struct import unpack
import pprint


def bytes_to_number(b):
    # if Python2.x
    # b = map(ord, b)
    res = 0
    for i in range(4):
        res += b[i] << (i*8)
    return res


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
  

port = 12345                
  
s.connect(('127.0.0.1', port)) 

print ("\n\t\t\t\tNANODB")
print ("\t\t\t    -------------")

          
print (s.recv(1024).decode())

while 1:                                                    #outer loop breaks on exit.contains 2 prompts

    while 1:                                                #prompt for login and register.loops till successful login or exit                
        command = input("--->")                             
        s.send(command.encode())
        if command=="exit":
            break
        if command=="login" or command=="register":
            username=input("Enter username: ")
            password=getpass.getpass()
            s.send(username.encode())
            s.send(password.encode())
        data = s.recv(1024).decode()
        print (data)
        if data=="Successfully logged in":
            break

    if command=="exit":
        break
    
    while 1:                                                #query loop breaks on exit and logout
        query=input(username+">>")
        s.send(query.encode())
        if query=="logout" or query=="exit":
            break
        signal = s.recv(4) 
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

    if query=="exit":                                                   #exits from program
        break
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
            current_size += len(data)
            print (data)
            """
s.close()
