import socket, threading, time, os

#send function


def sendMessages(msg, destination):
  HOST = destination  # The server's hostname or IP address
  PORT = 65432        # The port used by the server

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((HOST, PORT))
      s.sendall(msg)
      data = s.recv(1024)

      s.close()
      #break

  return repr(data)

#a receive function

def getMessages(sender):
  HOST = sender
  PORT = 65432

  message = b""

  value = ''

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

        if data.decode("utf-8") != '1234':
          print(data.decode("utf-8"))

        value = data

        if data == b'q':
          conn.close()
          break
        if data == b'1234':
          conn.sendall(b'1234')
        else:
          conn.sendall(b'received')

  return value


#try/except loop that starts the threads and runs the functions

#getMessages('127.0.0.1')
def runGet(otherIP):

  myName = ''

  if (getMessages(otherIP) == b'1234'):

    response = b''

    while True:
      
      response = getMessages(otherIP)

      #sendMessages(b'sTaRtInGtHePrOgRaM', '10.24.103.101')
      if (response == b'bye'):

        choice = input("User has left the chat the chat, would you like to exit?")

        os._exit(0)

        break

def runSend(otherIP):

  exit = 'bye'

  if sendMessages(b'1234', otherIP) == "b'1234'":

    print('Connection Successful\n')

    name = input('Enter your name: ')

    while True:

      msg = name + ': ' + input()

      if msg == name + ': bye':
        sendMessages(exit.encode("utf-8"), otherIP)
        print('You have left the conversation')
        break

      sendMessages(msg.encode("utf-8"), otherIP)

  os._exit(0)


print('Welcome to GCC IM')
otherIP = input('Enter the other IP: ')
print('Trying to connect...')

get = threading.Thread(target=runGet, args=(otherIP,))
send = threading.Thread(target=runSend, args=(otherIP,))
connected = False
tryConnection = 1
maxTries = 20

while not (connected):
  try:
    send.start()
    get.start()
    connected = True
  except:
    if(tryConnection > maxTries):
      print("Could not connect to that IP address...")
      break
    tryConnection = tryConnection + 1
    time.sleep(1)

