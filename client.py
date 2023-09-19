# client.py
# This code explains how to create a socket object to create a client
import socket
import threading as th

# AF_Inet for IPV4 and SOCK_STREAM for TCP/IP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send():
    while True:
        try:
            msg = input()
            s.send(msg.encode())
        except:
            break
def recv():
    while True:
        try:
            msg = s.recv(1024).decode()
            if msg != '':
                print(msg)
        except:
            print("in except")
            #s.close()
            break

# write the server IP and port number
ip = "172.20.10.4"
port = 1234
# connect to the server
s.connect((ip, port))
# Receive message from the server
message = s.recv(1024)
print(message.decode())
#enter name of client
name = input()
#send name to server
s.send(name.encode())
# Receive message from the server
message = s.recv(1024)
print(message.decode())
#create send and recv threads
send_thread = th.Thread(target=send)
recv_thread = th.Thread(target=recv)

#start threads
send_thread.start()
recv_thread.start()
