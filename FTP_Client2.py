import socket

#requests server IP address to connect
userIP = input(("What is the server's IP address"))

def client(ipAddress):
    
    #connects to server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((ipAddress, 2222))
    
    print("Welcome to GCC FTP client!\n")
    
    print("The available commands are:/nLIST/nSIZE/nSTOR/nRETR/nQUIT/n")
    
    #allows user to send commands while connected to server
    while True:
        cmd = input("COMMAND>> ")
        #sends command to server
        s.sendall(cmd.encode())
        
        cmdInput = cmd.split(' ')
        
        #sends file to server if file is requested from server
        if(cmdInput[0] == "STOR"):
            file = open(cmdInput[1], "rb")
            
            data = file.read(1024)
            while data:
                s.send(data)
                file.read(1024)
        
        #gets and prints out reply from server
        reply = s.recv(1024)
        print("FS: \n" + reply.decode() + "\n")
        
        
        #terminates client connection if server connection is terminated
        if reply.decode() == 'Connection terminated':
            s.close()
            break;
            
            
client(userIP)