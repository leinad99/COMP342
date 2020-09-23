import socket, threading, time, os

#send function
def sendMessages(msg, destination):
  HOST = destination  # The server's hostname or IP address
  PORT = 65432        # The port used by the server

  #create a connection for message sending
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((HOST, PORT))
      s.sendall(msg)

      #receive the message
      data = s.recv(1024)

      #close the connection
      s.close()
      #break

  #return the data sent back
  return repr(data)

# receive function
def getMessages(sender):
  HOST = sender
  PORT = 65432

  #variable initialization
  message = b""

  value = ''

  #create a connection for receiving messages
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', PORT))
    s.listen()
    #print('Socket is listening on port 65432')
    conn, addr = s.accept()
    with conn:
      #print('Connected by' , addr)
      while True:
        data = conn.recv(1024)
        if not data:
          break

        #decode the data from a bit literal string
        if data.decode("utf-8") != '1234':
          print(data.decode("utf-8"))

        value = data

        #check the type of messages to decide what to do
        if data == b'1234':
          conn.sendall(b'1234')
        else:
          conn.sendall(b'received')
  #return the message received
  return value


#try/except loop that starts the threads and runs the functions

#getMessages('127.0.0.1')

#function for the getMessages thread
def runGet(otherIP):

  myName = ''

  #initialize the connection
  if (getMessages(otherIP) == b'1234'):

    response = b''

    while True:
      
      response = getMessages(otherIP)

      #sendMessages(b'sTaRtInGtHePrOgRaM', '10.24.103.101')

      #Tell the thread to exit when another user leaves
      if (response == b'bye'):
        print('User has left the chat')

        os._exit(0)

        break
#function for the sendMessages thread
def runSend(otherIP):

  exit = 'bye'

  #ininitalize the connection

  if sendMessages(b'1234', otherIP) == "b'1234'":

    print('Connection Successful\n')

    name = input('Enter your name: ')

    #while loop that runs until the user decides to exit
    while True:
      #does not do input(name + ': ') because it leads to the formatting looking
      #even worse if the remote user happens to send a message while the local user is typing
      msg = name + ': ' + input()

      #check if the user wants to leave the chat
      if msg == name + ': bye':
        sendMessages(exit.encode("utf-8"), otherIP)
        print('You have left the conversation')
        break

      sendMessages(msg.encode("utf-8"), otherIP)

  os._exit(0)



#Welcome screen and initial data gathering
print('Welcome to GCC IM')
otherIP = input('Enter the other IP: ')
print('Trying to connect...')

#run the threads to get and send messages simultaneously
get = threading.Thread(target=runGet, args=(otherIP,))
send = threading.Thread(target=runSend, args=(otherIP,))
connected = False
tryConnection = 1 #number of times you've tried to connect
maxTries = 20 #try 20 times to connect

while not (connected):
  try:
    send.start()
    get.start()
    #if both methods started successfuly, exit out of loop
    connected = True
  except:
    if(tryConnection > maxTries):
      print("Could not connect to that IP address...")
      break
    #if not, add one to number of times trying to connect, wait 1 second, and try again
    tryConnection = tryConnection + 1
    time.sleep(1)

