import socket, os, time


#connects to other server to receive input
def client(ip):
    
    #creates socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connects to server
    s.connect((ip, 2222))
    print("Connected")
    while True:
        cmd = input("COMMAND>> ")
        #sends command to server
        s.sendall(cmd.encode())
        
        #parses command sent to server
        cmdInput = cmd.split(' ')

        #code for RETR command
        if(cmdInput[0] == "RETR"):
          #opens file to be written to
          file = open(cmdInput[1],'wb')
          
          #writes file contents retrieved from server to current directory
          sizeStr = s.recv(1024)
          size = int(sizeStr.decode())
          readBytes = 0
          while readBytes < size:
              data = s.recv(1024)
              readBytes += len(data)
              file.write(data)
        
          file.close()

        #code for STOR command
        if(cmdInput[0] == "STOR"):
            #opens file to be read to server
            file = open(cmdInput[1], "rb")
            path = os.getcwd() + '\\' + cmdInput[1]
            #finds size of file and sends to server
            size = str(os.path.getsize(path))
            s.sendall(size.encode())
            #delays sending file contents so server can fully receive size
            time.sleep(1)
            
            #reads and sends file contents to server
            data = file.read(1024)
            while data:
              s.send(data)
              data = file.read(1024)
            file.close()

        #prints reply messages from server
        print("FS:")
        while(True):
          reply = s.recv(1024)
          print(reply.decode())
          if not reply or len(reply) < 1024:
            break
        
        #terminates connection when server does
        if reply.decode() == 'Connection terminated':
            s.close()
            break

print("Welcome to GCC FTP Client!")
userIP = input(("What is the server's IP address: "))
client(userIP)