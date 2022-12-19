import smtplib

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

reciever = "anderseriksen02@gmail.com"
email = "trondertrip@yahoo.com"
password = "testmail123"
# Authentication
s.login(email, password)

# message to be sent
message = "This is a test"
# sending the mail
s.sendmail(email, reciever, message)
print("Mail sent")

# terminating the session
s.quit()
