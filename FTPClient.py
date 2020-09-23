import socket
import sys

s = socket.socket()
s.connect(("localhost",2222))
f = open ("I can do this all day.jpg", "rb")
l = f.read(1024)
while (l):
    s.send(l)
    l = f.read(1024)
s.close()
