import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SENDER = os.getenv("GMAIL_SENDER")
PASSWORD = os.getenv("GMAIL_PASSKEY")


def send_mail(subject: str, html_body: str, recipients: [str]):
    mail = MIMEMultipart("alternative")
    mail["Subject"] = subject
    mail["From"] = SENDER
    mail["To"] = ", ".join(recipients)
    mail.attach(MIMEText(html_body, "html"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(SENDER, PASSWORD)
        smtp_server.sendmail(SENDER, recipients, mail.as_string())


if __name__ == '__main__':
    sj = ""
    send_mail(sj, "<h1>test</h1>", ["aquashdw@gmail.com"])
