
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib
import keys


def send_mail(subject: str, body: str, email_sender: str, email_reciever: str, email_app_password: str, html: bool = False) -> None:
    email = MIMEMultipart('alternative')
    email['From'] = email_sender
    email['To'] = email_reciever
    email['Subject'] = subject
    if html:
        part = MIMEText(body, 'html')
    else:
        part = MIMEText(body, 'plain')
    email.attach(part)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender, email_app_password)
        smtp.sendmail(email_sender, email_reciever, email.as_string())
