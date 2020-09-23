import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.37.113.194', 80))

#s.send(b'PUT /led/flashAlarm HTTP/1.1\r\n\r\n')
#s.send(b'PUT /led/lightsOn HTTP/1.1\r\n\r\n')
#s.send(b'PUT /led/lightsOff HTTP/1.1\r\n\r\n')
#s.send(b'GET /sensors/proximity HTTP/1.1\r\n\r\n')
s.send(b'GET /sensors/temperature HTTP/1.1\r\n\r\n')

reply = s.recv(1024)

print(reply.decode())