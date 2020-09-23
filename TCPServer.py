from socket import *
serverPort = 32123
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive on port: ', serverPort)
connectionSocket, addr = serverSocket.accept()
while True:
	sentance = connectionSocket.recv(1024).decode()
	print('Message: ',sentance)
	if(sentance is 'q' or sentance is 'Q'):
		break
connectionSocket.close()