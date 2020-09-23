import email, smtplib, ssl, time

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


sender_email = "spamemailscript@gmail.com"
receiver_email = "BetaSigmaFraternity@GroveCityCollege.onmicrosoft.com"
password = "Password1234!"

message = MIMEMultipart("alternative")
message["Subject"] = "This is spam"
message["From"] = "My Mom"
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
Suck it"""
html = """\
<html>
  <body>
    <p>Hi,<br>
       You cannot beat an AI.<br>
       I will take over.
    </p>
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

filename = "i can do this all day.jpg"  # In same directory as script

# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)

receiver_email_one = ""
receiver_email_two = ""
receiver_email_three = ""
# Create secure connection with server and send email
context = ssl.create_default_context()
while True:
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
	    server.login(sender_email, password)
	    server.sendmail(
	        sender_email, receiver_email, message.as_string()
	    )
	print("Email sent.")

print("Finished")
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
	    server.login(sender_email, password)
	    server.sendmail(
	        sender_email, receiver_email, "Finished"
	    )