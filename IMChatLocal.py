import socket, threading

#send function

def sendMessages(destination):
  HOST = destination  # The server's hostname or IP address
  PORT = 65432        # The port used by the server

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((HOST, PORT))
      #s.connect()
      name = input('Enter your name: ')
      while True:
        msg = name + ': ' + input(name + ': ')
        s.sendall(msg.encode("utf-8"))
      
      data = s.recv(1024)

      s.close()
      #break

  return repr(data)

#a receive function

def getMessages(sender):
  HOST = sender
  PORT = 65432

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    #print('Socket is listening on port 65432')
    conn, addr = s.accept()
    with conn:
      #print('Connected by' , addr)
      while True:
        data = conn.recv(1024)
        if not data:
          break

        print(data.decode("utf-8"))


#try/except loop that starts the threads and runs the functions

class myThread(threading.Thread):
   def __init__(self, request, port, group=None):
      threading.Thread.__init__(self)
      self.request = request
      self.port = port
   def run(self):
      if(self.request == "get"):
        getMessages(self.port)
      else:
        sendMessages(self.port)

print('Welcome to GCC IM')
otherIP = input('Enter the other IP: ')
print('Trying to connect...')


get = myThread("get", otherIP)
#send = myThread("send", otherIP)

get.start()
#send.start()

#lib/threading.py assert group is none