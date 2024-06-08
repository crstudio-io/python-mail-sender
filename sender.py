import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

subject = "test subject"
body = "<h1>Hello</h1>"
sender = "aquashdw@gmail.com"
recipients = ["aquashdw@gmail.com"]
password = os.getenv("GMAIL_PASSKEY")

msg = MIMEMultipart('alternative')
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = ", ".join(recipients)
msg.attach(MIMEText(body, "html"))
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
