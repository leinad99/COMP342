# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 18:47:42 2019

@author: DEGRAAFDJ1
"""

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Listening on port " + str(PORT))
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            if(data == b'q'):
                conn.close()
                break