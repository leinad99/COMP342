#Initalize all imports
import socket, time, getpass
from threading import Thread
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#global varaibles
keepLoggingTemp = True #global variable to stop the logging temperature thread
keepLoggingProx = True #global variable to stop the logging proximity thread
startedLoggingTemp = False #variable to keep track if you have started a logging temperature thread
startedLoggingProx = False #variable to keep track if you have started a logging proximity thread
setPassword = False #Variable to keep track if you have set a password for the actuator values or not
alarmSet = False #Variable to keep track if the alarm is set
start = 0 #Time variable
proximityKey = "NOT PRESENT" #Key to check alarm
tempKey = 50.00 #Key to check alarm
#ipAddress = '' #ip address of the arduino board
password = 'Password1234' #password needed to control the lights
gotPassword = False #if the user has put in the password this session
maxTemp = 100 #highest the temperature can be efore triggering the alarm
minTemp = 32 #lowest the temperature can be before trigering the alarm

#Every 15 seconds check the alarm conditions
def checkAlarm(s):
    #declare so we can use these
    global alarmSet 
    global maxTemp
    global minTemp
    #While alarm is set...
    while (alarmSet):
        #Get proximity sensor data
        s.send(b'GET /sensors/proximity HTTP/1.1\r\n\r\n')
        time.sleep(1)
        reply = s.recv(1024)
        proximityKey = reply.decode()
        #get temperature sensor data
        s.send(b'GET /sensors/temperature HTTP/1.1\r\n\r\n')
        time.sleep(1)
        reply = s.recv(1024)
        tempString = reply.decode()
        #Reply is four lines, and only fourth line has data so, take only the fourth line
        tempString = tempString.splitlines()[3]
        #Create two placement counters
        counter1 = 0 #Beginning of number
        counter2 = 0 #Ending of number
        #Start at beginning of string and iterate through all characters in the string
        #While character is not a number, check others
        while(not tempString[counter1].isdigit()):
            counter1 = counter1 + 1
        #Found beginning of number, now get the ending number pointer to this
        counter2 = counter1
        #While the ending pointer is still pointing to a number
        #move the pointer to the next digit
        while(tempString[counter2].isdigit()):
            counter2 = counter2 + 1
        #Make the temp key the substring with the beginning that first number and ends right
        #when there is a non-digit
        tempKey = int(tempString[counter1:counter2])
        
        #If either of these is set, send email
        if(proximityKey.find("NOT") == -1):
            sendEmail(s, "window and door proximity sensor has been triggered")
            alarmSet = False
        elif(tempKey > maxTemp):
            sendEmail(s, "temperature is above above " + str(maxTemp) +" degrees in your house")
            alarmSet = False
        elif(tempKey < minTemp):
            sendEmail(s,  "temperature is above below " + str(minTemp) + " degrees in your house")
            alarmSet = False
        
        #Wait for 13 more seconds, alreadyslept for 2 seconds
        time.sleep(13)
    

def logTemp(s):
    #log the temperature every 5 seconds
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    file = open("loggingTempData.txt","w") #open the file
    file.write("Started logging temperature data on " + dt_string + "\n\n") #write a header line with date and time
    while True:
        s.send(b'GET /sensors/temperature HTTP/1.1\r\n\r\n')
        time.sleep(1)
        reply = s.recv(1024)
        file.write(reply.decode().splitlines()[3] + "\n") #put the message into the file
        time.sleep(5)
        #so the user can stop logging the information
        global keepLoggingTemp
        if not keepLoggingTemp:
            file.close()
            break

def logProx(s):
    #log the proximity sensor every 5 seconds
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    file = open("loggingProxData.txt","w") 
    file.write("Started logging proximity sensor data on " + dt_string + "\n\n")
    while True:
        s.send(b'GET /sensors/proximity HTTP/1.1\r\n\r\n')
        time.sleep(1)
        reply = s.recv(1024)
        file.write(reply.decode().splitlines()[3] + "\n")
        time.sleep(5)
        global keepLoggingProx
        if not keepLoggingProx:
            file.close()
            break

def sendEmail(s, triggeringAlarm):
    #FLASH ALARM
    s.send(b'PUT /led/flashAlarm HTTP/1.1\r\n\r\n')
    time.sleep(1)
    s.recv(1024)
    #Get email credentials
    sender_email = "comp342gccf19@gmail.com"
    receiver_email = "comp342gccf19@gmail.com"
    password = "P@$$word1!"

    #Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "WARNING: ALARM SET OFF"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    User,
    One of the alarm conditions has been set off in your system.
    This is a notification.
    Hodge and DeGraaf Security Systems"""
    html = """\
    <html>
      <body>
        <p>
        User,
        The """ + triggeringAlarm + """ and has set off in your system.
        This is a notification.
        </p>
        <h2>
        Hodge and DeGraaf Security Systems
        </h2>
      </body>
    </html>
    """
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

print("Welcome to DeGraaf and Hodge Home Security!\n")
ipAddress = input("Please type in the IP Address of the home security web server: ")
print("Connecting...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ipAddress, 80))
print("Connected!\n")
#Opening message 

print("Here's a list of commands you can do:")
print("Turn on your exterior lights with 'LIGHTS ON'")
print("Turn off your exterior lights with 'LIGHTS OFF'")
print("FLash the alarm in the house with 'FLASH ALARM'")
print("Check the temperature of the house with 'TEMP'")
print("Check the calue of the proximity sensor in the house with 'PROX'")
print("Check the value of all the sensors in the house with 'ALL'")
print("Turn on the alarm with 'ALARM ON'")
print("Turn on the alarm with 'ALARM OFF'")
print("Start logging data with 'START LOG TEMP'")
print("Stop logging data with 'STOP LOG TEMP'")
print("Start logging data with 'START LOG PROX'")
print("Stop logging data with 'STOP LOG PROX'")
print("List the hardware you have installed with 'LIST'")
print("Exit out of service with 'EXIT'\n")
#print("Check to see if your doors and windows are closed with DRAFT") 
#Check to see if this is needed

#initilize exit and command variables
shouldExit = False
command = ""
#Until the program should exit
while(not shouldExit):
    #Get user commands
    command = input("\nEnter command: ")
    #Exit program
    if(command == "EXIT"):
        shouldExit = True
    #Turn lights on
    elif(command == "LIGHTS ON"):
        #check if the user has entered a password for this session yet
        if(gotPassword):
            s.send(b'PUT /led/lightsOn HTTP/1.1\r\n\r\n')
            time.sleep(1)
            s.recv(1024)
            print("Turned on lights")
        #else, get the password from the student 
        else:
            p = getpass.getpass("What is your home security system password: ")
            if(p == password):
                gotPassword = True
                s.send(b'PUT /led/lightsOn HTTP/1.1\r\n\r\n')
                time.sleep(1)
                s.recv(1024)
                print("Turned on lights")
            else:
                print("The password '" + p + "' is incorrect.")
    #Turn lights off
    elif(command == "LIGHTS OFF"):
        #same logic as lights on
        if(gotPassword):
            s.send(b'PUT /led/lightsOff HTTP/1.1\r\n\r\n')
            time.sleep(1)
            s.recv(1024)
            print("Turned off lights\n")
        else:
            p = getpass.getpass("What is your home security system password: ")
            if(p == password):
                gotPassword = True
                s.send(b'PUT /led/lightsOff HTTP/1.1\r\n\r\n')
                time.sleep(1)
                s.recv(1024)
                print("Turned off lights\n")
            else:
                print("The password '" + p + "' is incorrect.")
    elif(command == "FLASH ALARM"):
        #same logic as lights on
        if(gotPassword):
            s.send(b'PUT /led/flashAlarm HTTP/1.1\r\n\r\n')
            time.sleep(1)
            s.recv(1024)
            print("Flashed the alarm")
        else:
            p = getpass.getpass("What is your home security system password: ")
            if(p == password):
                gotPassword = True
                s.send(b'PUT /led/flashAlarm HTTP/1.1\r\n\r\n')
                time.sleep(1)
                s.recv(1024)
                print("Flashed the alarm")
            else:
                print("The password '" + p + "' is incorrect.")
    #Set Alarm
    elif(command == "ALARM ON"):
        #check if a alarm is already set
        if not alarmSet:
            #Print current value of the sensors 
            s.send(b'GET /sensors/proximity HTTP/1.1\r\n\r\n')
            time.sleep(1)
            reply = s.recv(1024)
            print(reply.decode().splitlines()[3])
            s.send(b'GET /sensors/temperature HTTP/1.1\r\n\r\n')
            time.sleep(1)
            reply = s.recv(1024)
            print(reply.decode().splitlines()[3])

            alarmSet = True
            alarmThread = Thread(target = checkAlarm, args =(s, )) 
            alarmThread.start()  
            print("Turned on alarm")
        else:
            print("Alarm already turned on.")
    #Unset alarm
    elif(command == "ALARM OFF"):
        if alarmSet and alarmThread.is_alive():
            alarmSet = False
            alarmThread.join()
            print("Turned off alarm")
        else:
            print("Alarm is not set.")
    #See temperature of house
    elif(command == "TEMP"):
        s.send(b'GET /sensors/temperature HTTP/1.1\r\n\r\n')
        time.sleep(1)
        reply = s.recv(1024)
        #print("WHOLE MESSAGE : " + reply.decode())
        print(reply.decode().splitlines()[3])
    #See proximity sensor value of house
    elif(command == "PROX"):
        s.send(b'GET /sensors/proximity HTTP/1.1\r\n\r\n')
        time.sleep(1)
        reply = s.recv(1024)
        print(reply.decode().splitlines()[3])
    #get value of all sensors
    elif(command == "ALL"):
        s.send(b'GET /sensors/proximity HTTP/1.1\r\n\r\n')
        time.sleep(1)
        reply = s.recv(1024)
        print(reply.decode().splitlines()[3])
        s.send(b'GET /sensors/temperature HTTP/1.1\r\n\r\n')
        time.sleep(1)
        reply = s.recv(1024)
        print(reply.decode().splitlines()[3])
    #Start logging the temperature of the house
    elif(command == "START LOG TEMP"):
        #check if you are already logging the temperature
        if not startedLoggingTemp:
            startedLoggingTemp = True
            print("Logging Started")
            s.send(b'GET /sensors/temperature HTTP/1.1\r\n\r\n')
            time.sleep(1)
            reply = s.recv(1024)
            print(reply.decode().splitlines()[3])
            keepLoggingTemp = True
            tempThread = Thread(target = logTemp, args=(s, )) 
            tempThread.start()  
        else:
            print("Already logging the temperature")
    #Stop logging the temperature of the house
    elif(command == "STOP LOG TEMP"):
        if startedLoggingTemp and tempThread.is_alive(): 
            keepLoggingTemp = False
            startedLoggingTemp = False
            tempThread.join()
            print("Stopped logging information")
            s.send(b'GET /sensors/temperature HTTP/1.1\r\n\r\n')
            time.sleep(1)
            reply = s.recv(1024)
            print(reply.decode().splitlines()[3])
        else: 
            print('No existing logging thread found') 
    #Start logging the proximity sensor of the house
    elif(command == "START LOG PROX"):
        if not startedLoggingProx:
            startedLoggingProx = True
            print("Logging Started")
            s.send(b'GET /sensors/proximity HTTP/1.1\r\n\r\n')
            time.sleep(1)
            reply = s.recv(1024)
            print(reply.decode().splitlines()[3])
            keepLoggingProx = True
            proxThread = Thread(target = logProx, args=(s, ))
            proxThread.start()  
        else:
            print("Already logging the poximity threading")
    #Stop logging the proximity sensor of the house
    elif(command == "STOP LOG PROX"):
        if startedLoggingProx and proxThread.is_alive():
            keepLoggingProx = False
            startedLoggingProx = False
            proxThread.join()
            print("Stopped logging information")
            s.send(b'GET /sensors/proximity HTTP/1.1\r\n\r\n')
            time.sleep(1)
            reply = s.recv(1024)
            print(reply.decode().splitlines()[3])
        else: 
            print('No existing prox thread found') 
    #List hardware availible
    elif(command == "LIST"):
        print("The hardware you have availible to you are as follows...")
        print("Home lights connected at pin D1")
        print("Window and door detection connected at pin D4")
        print("Thermostat connected at pin D5")
        print("Flashing alarm connected at pin D2")
    #Command not known, so show list of commands possible
    else:
        print("Command not supported.  Here's a list of commands possible.")
        print("LIGHTS ON")
        print("LIGHTS OFF")
        print("FLASH ALARM")
        print("TEMP")
        print("PROX")
        print("ALL")
        print("ALARM ON")
        print("ALARM OFF")
        print("START LOG TEMP")
        print("STOP LOG TEMP")
        print("START LOG PROX")
        print("STOP LOG PROX")
        print("LIST\n")
print("Stopping service.")


    
    
