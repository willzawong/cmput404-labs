#!/usr/bin/env python3
import socket
import time
import sys
from multiprocessing import Process

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information   
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    proxy_host = "127.0.0.1"
    proxy_port = "8001"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            # new socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_s:
                p = Process(target=proxy_handler,args=(conn,proxy_s))
                p.daemon=True
                p.start()

                
            while True:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    break
                response_data += data

                conn.sendall(response_data)
                
            conn.close()

def proxy_handler(conn,proxy_s):
    #recieve data, wait a bit, then send it back
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    conn.sendall(full_data)
    time.sleep(0.5)
    proxy_s.shutdown(socket.SHUT_WR)

if __name__ == "__main__":
    main()
