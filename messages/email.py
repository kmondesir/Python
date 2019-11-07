


import sys
import os
import datetime as dt
import smtplib, ssl, email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create a secure SSL context
context = ssl.create_default_context()

import logging as log
severity = {
            'CRITICAL': 50,
            'ERROR': 40,
            'WARNING': 30,
            'INFO': 20,
            'DEBUG': 10,
            'NOTSET': 0,
}

logger = log.getLogger(__name__)
formatter = log.Formatter('timestamp:%(asctime)s module:%(name)s message:%(message)s')

filename = os.path.splitext(__file__)[0]
extension = "log"
file_handler = log.FileHandler(filename + "." + extension)
file_handler.setLevel(severity["INFO"])
file_handler.setFormatter(formatter)

stream_handler = log.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class mail:

  """
  Opens a file for reading, writing and updating

  The code references a video 'Python Tutorial: Context Managers - Efficiently Managing Resources' 
  created by Corey Schafer and is part of a video series

  https://www.youtube.com/redirect?redir_token=tKiuOsI1ZF8oNIDLKASs2PhnbWZ8MTU3MDk5ODI1M0AxNTcwOTExODUz&q=https%3A%2F%2Fgithub.com%2FCoreyMSchafer%2Fcode_snippets%2Ftree%2Fmaster%2FPython-Context-Managers&v=-aKFBoZpiqA&event=video_description
  
  https://www.daniweb.com/programming/software-development/threads/191670/saving-to-creating-a-new-folder 
  """

  def __init__(self, username, server='smtp.gmail.com', port=587):
    # https://realpython.com/python-send-email/
    self.username = username
    self.password = input("Please enter your password: ")
    self.server = server
    self.port = port
    
    try:
      self.mail = smtplib.SMTP(self.server, self.port)
      self.mail.starttls()
      self.mail.login(self.username, self.password)      
    except Exception as e:
      logger.error(e)
    else:
      pass

  def sender(self, sender=self.username):
    self.sender = sender

  def receivers(self, receiver=self.username, carbon_copy=None, blind_carbon_copy=None):
    self.carbon_copy = carbon_copy
    self.blind_carbon_copy = blind_carbon_copy
    
  def message(self, subject='Default message sent at {}'.format(dt.datetime.now()), body=None):
    self.subject = subject
    self.body = body

  def send(self):
    
    try:
      msg = MIMEMultipart("alternative")
      if self.carbon_copy:
        msg["Cc"] = self.carbon_copy
      elif self.blind_carbon_copy:
        msg["Bcc"] = self.blind_carbon_copy
      # sets up message variables
      msg["To"] = self.receiver
      msg["From"] = self.sender
      msg["Subject"] = self.subject
      
      # add in the message body
      msg.attach(MIMEText(self.body, 'plain'))
    except Exception as e:
      logger.error(e)
    else:
      self.mail.send_message(msg)
    finally:
      self.mail.quit()