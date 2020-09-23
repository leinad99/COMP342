from socket import *
server_port = 32123
server_name = '127.0.0.1'
client_socket = socket(AF_INET, SOCK_STREAM)

client_socket.connect((server_name, server_port))
print('Enter (q or Q) to exit')
while True:
	message = input('Enter a message: ')
	client_socket.send(message.encode())
	if(message is 'Q' or message is 'e'):
		break
client_socket.close()
