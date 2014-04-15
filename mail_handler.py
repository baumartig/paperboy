from settings_handler import settings
import os
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64

def sendMail(subject, text, *attachmentFilePaths):

  recipient = settings.mailTo
  sender = settings.mailFrom
  msg = MIMEMultipart('mixed')
  msg['From'] = sender
  msg['To'] = recipient
  msg['Subject'] = subject
  msg.attach(MIMEText(text))
  print "Start sending mail:"
  print "Recipient: %s" % recipient
  print "Sender: %s" % sender
  print "Subject: %s" % subject
  print "Recipient: %s" % recipient


  for attachmentFilePath in attachmentFilePaths:
    msg.attach(getAttachment(attachmentFilePath))

  if settings.useSmtp():
    if "port" in settings.smtpServer:
        mailServer = smtplib.SMTP(    settings.smtpServer["address"],
                                    settings.smtpServer["port"])
    else:
        mailServer = smtplib.SMTP(settings.smtpServer["address"])

    if "security" in settings.smtpServer:
        if settings.smtpServer["security"] == "starttls":
            # handle starttls
            gmailUser = settings.smtpServer["login"]
            gmailPassword = settings.smtpServer["password"]
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(gmailUser, gmailPassword)
  else:
    print "Using sendmail"
    mailServer = smtplib.SMTP('localhost')

  print "Sending mail"
  mailServer.set_debuglevel(1)
  mailServer.sendmail(sender, recipient, msg.as_string())
  mailServer.close()

def getAttachment(attachmentFilePath):
  contentType, encoding = mimetypes.guess_type(attachmentFilePath)
  if contentType is None or encoding is not None:
    contentType = 'application/octet-stream'
  mainType, subType = contentType.split('/', 1)
  file = open(attachmentFilePath, 'rb')
  if mainType == 'text':
    attachment = MIMEText(file.read())
  elif mainType == 'message':
    attachment = email.message_from_file(file)
  elif mainType == 'image':
    attachment = MIMEImage(file.read(),_subType=subType)
  elif mainType == 'audio':
    attachment = MIMEAudio(file.read(),_subType=subType)
  else:
    attachment = MIMEBase(mainType, subType)
  attachment.set_payload(file.read())
  encode_base64(attachment)
  file.close()
  attachment.add_header('Content-Disposition', 'attachment',   filename=os.path.basename(attachmentFilePath))
  return attachment
