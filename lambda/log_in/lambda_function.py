import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
import smtplib
from g_password import get_password
from email.mime.text import MIMEText

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

body = "Someone has been attempting to log into your account. Please make sure you are using a secure password."
sender = "billmatesmail@gmail.com"

def check_database(data: dict) -> bool:
    query = {'email':data['email']}
    return mongo.query_user(query, True)
    
def lambda_handler(event, context):
    
    # Parameters
    payload = json.loads(event['body'])
    
    # Build reponse JSON
    response = {}

    # Verify token is correct before running more commands
    token = event['headers']['token']
    response["token_success"] = api.check_token(token)
    
    # Match against database
    if response["token_success"]:
        user, users = check_database(payload)
        response['login_success'] = (user != None) and (user['password'] == payload['password'])
        attempts = {"$set": {"attempts": 0} }
        if response['login_success']:
            response['user_data'] = {
                "email" : user['email'],
                "name" : user['name'],
                "groups" : user['groups'],
                "settings" : user['settings'],
            }
            users.update_one(user, {"$set": { "attempts": 0} })
        else:
            if user != None:
                new_attempts = user['attempts'] + 1
                response['user_data'] = {'attempts' : new_attempts}
                if new_attempts >= 3:
                    send_email("Suspicious Activity | BillMates", body, sender, [user['email']], get_password())
                    users.update_one(user, {"$set": { "attempts": 0} })
                else:
                    users.update_one(user, {"$set": { "attempts": user['attempts'] + 1} })
            else:
                response = {"ERROR" : "No user found"}
    else:
        response['login_success'] = False
    
    return api.build_capsule(response)