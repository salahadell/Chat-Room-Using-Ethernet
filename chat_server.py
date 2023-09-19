# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 09:55:21 2023

@author: salah
"""

import socket as so
import threading as th


server=so.socket(so.AF_INET,so.SOCK_STREAM)
# set the ip of the server device
ip="172.20.10.4"
# set the port number of the server device
port=1234
server.bind((ip,port))
# set the max number of clients to be connected
server.listen(5)

clients=[]
clients_names=[]
rec_thread=[]

def receive(client):
    while 1:
            try:
                 rec= client.recv(1024).decode()
                 mess=clients_names[clients.index(client)]+": "+rec
                 broadcast(mess,clients_names[clients.index(client)])
            except:
                # disconnect the client if he doesn't send any message before the timeout period
                print(f"{clients_names[clients.index(client)]} is disconnected")
                #rec_thread[clients.index(client)].close()
                clients_names.pop(clients.index(client))
                clients.remove(client)
                client.close()
                break
  
            
def accept():
    while 1:
        client, address=server.accept()
        # set timeout for each client to disconnect them if anyone of them doesn't send any message before the timeout period
        client.settimeout(100)
        # append each new client to the clients' list
        clients.append(client)
        client.send("Salah's Server': Send Your Name".encode())
        try:
        # append each new client name to the clients names' list
            clients_names.append(clients[-1].recv(1024).decode("utf-8"))
            print(f"{clients_names[-1]} joined the room")
            broadcast(f"{clients_names[-1]} joined the room",clients_names[-1])
            rec_thread.append(th.Thread(target=receive,args=(client,)))
            rec_thread[-1].start()
        except:
            clients[-1].close()
            print(f"{clients[-1]} is disconnected")
            clients.pop(-1)


         
            
        
def broadcast(message,sender_name):
    # send the messages from client to the other clinet in the chat room
    for client in clients:
        if sender_name ==  clients_names[clients.index(client)]:
          continue
        else:
           client.send(message.encode())
  
# run the server and waiting for clients to connect            
print("server is running")    
acc_thread= th.Thread(accept())
acc_thread.start()

