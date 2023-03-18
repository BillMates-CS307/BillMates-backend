import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.send as send
import bundle.thread as thread

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
        db = mongo.get_database()
        user = mongo.query_table('users', {'email': payload['email']}, db)
        users = db['users']
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
                    args = ("Suspicious Activity | BillMates", \
                    "Someone has been attempting to log into your account. Please make sure you are using a secure password.", \
                    [user['email']])
                    thread.fire(send.send_email, args)
                    users.update_one(user, {"$set": { "attempts": 0} })
                else:
                    users.update_one(user, {"$set": { "attempts": user['attempts'] + 1} })
            else:
                response = {"ERROR" : "No user found"}
    else:
        response['login_success'] = False
    
    return api.build_capsule(response)