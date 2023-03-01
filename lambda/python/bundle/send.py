from g_password import get_password
from email.mime.text import MIMEText
import smtplib

# Give a subject line (str), a body (the message), and a list of recipients (emails)

def send_email(subject: str, body: str, recipients: list) -> bool:
    sender = "billmatesmail@gmail.com"
    password = get_password()
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        smtp_server.quit()
        return True
    except:
        return False
