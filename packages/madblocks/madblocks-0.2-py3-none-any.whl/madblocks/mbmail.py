import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_with_attachment(username=None,password=None,receiver=None,imagefile=None,subject=None,body=None):
  print("Sending E-mail with Image Attachment")
  email_sender = username
  email_receiver = receiver
  msg = MIMEMultipart()
  msg['From'] = email_sender
  msg['To'] = email_receiver
  msg['Subject']= subject
  msg.attach(MIMEText(body, 'plain'))

  #FILE PART
  filename = imagefile
  attachment = open(filename, 'rb')
  part = MIMEBase('application', 'octet_stream')
  part.set_payload((attachment).read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition', 'attachment; filename= '+filename)
  msg.attach(part)
  #########

  text = msg.as_string()
  connection = smtplib.SMTP('smtp.gmail.com', 587)
  connection.starttls()
  connection.login(email_sender, password)
  connection.sendmail(email_sender, email_receiver, text )
  connection.quit()
  print("E-mail Sent")

def send_email(username=None,password=None,receiver=None,subject=None,body=None):
  print("Sending E-mail")
  email_sender = username
  email_receiver = receiver
  msg = MIMEMultipart()
  msg['From'] = email_sender
  msg['To'] = email_receiver
  msg['Subject']= subject
  msg.attach(MIMEText(body, 'plain'))
  text = msg.as_string()
  connection = smtplib.SMTP('smtp.gmail.com', 587)
  connection.starttls()
  connection.login(email_sender, password)
  connection.sendmail(email_sender, email_receiver, text )
  connection.quit()
  print("E-mail Sent") 
  
