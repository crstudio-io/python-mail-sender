import os
import smtplib

from email.mime.text import MIMEText

subject = "test subject"
body = "Email Body"
sender = "aquashdw@gmail.com"
recipients = ["aquashdw@gmail.com"]
password = os.getenv("GMAIL_PASSKEY")

msg = MIMEText(body)
msg["Subject"] = subject
msg['From'] = sender
msg['To'] = ', '.join(recipients)
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
