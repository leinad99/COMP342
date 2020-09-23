import socket, os, time

def server():
    print("Trying to connect...")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #connects to client
        s.bind(('', 2222))
        s.listen()
        #s.settimeout(2.0)
        conn, addr = s.accept()
        
        print("Connection successful!\n")
        print("Welcome to GCC FTP service!\n")
        print("Waiting for client commands...\n")
        
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                
                #parses client's response
                userInput = data.decode().split(' ')
                
                #code for LIST command
                if userInput[0] == 'LIST':
                    #gets contents from current directory
                    dirContents = os.scandir(os.getcwd())
                    files = ""
                    #gets files from current directory
                    for file in dirContents:
                        if file.is_file():
                            files += file.name + "\n"
                    #sends files to client
                    conn.sendall(files.encode())
                     
                #code for SIZE command
                if userInput[0] == 'SIZE':
                    #retrieves file from directory
                    path = os.getcwd() + '\\' + userInput[1]
                    #finds size of file
                    size = str(os.path.getsize(path)) + 'B'
                    #symbol = ' B'
                    #sends size of file to client
                    conn.sendall(size.encode())
                    
                #code for STOR command - MAY HAVE ERRORS
                if userInput[0] == 'STOR': 
                    #ask client if file can be overwritten
                    msg = ""
                    if os.path.exists(userInput[1]):
                        msg += 'Overwriting file...\n'
                
                    #saves file to current directory
                    file = open(userInput[1], 'wb')
                    sizeStr = conn.recv(1024)
                    
                    size = int(sizeStr.decode())
                    readBytes = 0
                    while readBytes < size:
                        contents = conn.recv(1024)
                        readBytes += len(contents)
                        file.write(contents)
                  
                    file.close()
                    msg += 'File stored correctly'
                    conn.sendall(msg.encode())
                        
                #code for RETR command
                if userInput[0] == 'RETR':
                    file = open(userInput[1],'rb')
                    path = os.getcwd() + '\\' + userInput[1]
                    #finds size of file
                    size = str(os.path.getsize(path))
                    conn.sendall(size.encode())
                    
                  
                    contents = file.read(1024)
                    while contents:
                        conn.send(contents)
                        contents = file.read(1024)
                    
                    file.close()
                    
                    time.sleep(1) #delay sending comment so it doesn't get missed by the client
                  
                    conn.sendall(b'Here is the contents of ' + file.name.encode())
                
                #code for QUIT command
                if userInput[0] == 'QUIT':
                    #lets client know connection is being terminated
                    conn.sendall(b'Connection terminated')
                    print("Connection terminated by client...\n")
                    #terminates connection
                    s.close()
server()