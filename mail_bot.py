
from email.message import EmailMessage
import ssl
import smtplib
import keys


def send_mail(subject: str, body: str, email_sender: str, email_reciever: str, email_app_password: str) -> None:
    email = EmailMessage()
    email['From'] = email_sender
    email['To'] = email_reciever
    email['Subject'] = subject
    email.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender, email_app_password)
        smtp.sendmail(email_sender, email_reciever, email.as_string())


email_sender = 'trondertrip@gmail.com'
email_app_password = keys.app_password

email_reciever = 'anderseriksen02@gmail.com'

subject = 'Test Message'

body = """
Just\nChecking\nThat\nThis\nStill\nWorks!
"""

send_mail(subject, body, email_sender, email_reciever, email_app_password)