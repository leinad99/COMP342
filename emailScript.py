import smtplib
import numpy as np

mailer = smtplib.SMTP_SSL('smtp.gmail.com', 465)

mailer.ehlo()

gmail_user = 'comp342gccf19@gmail.com'
gmail_password = 'P@$$word1!'

mailer.login(gmail_user, gmail_password)

myroot = np.sqrt(13)

msg1= "From: Daniel DeGraaf \r\nTo: Dr. Rumbaugh \r\nSubject: Lab 3 \r\nThe value of the square root of 13 is " + (str)(myroot) +"\r\n"

mailer.sendmail(gmail_user, gmail_user, msg1)