import requests

# Give a subject line (str), a body (the message), and a list of recipients (emails)

def send_email(subject, body, recipients):
    data = {
        'subject' : subject,
        'body' : body,
        'recipients' : recipients,
    }
    requests.post("https://bl2w4cvg6hrrtpkcgov4yozgue0icsmu.lambda-url.us-east-2.on.aws/", json=data, headers={})