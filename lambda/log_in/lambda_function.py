import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo

def check_database(data: dict) -> bool:
    query = {'email':data['email'], 'password':data['password']}
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
        response['login_success'] = user != None
        attempts = {"$set": {"attempts": 0} }
        if response['login_success']:
            response['user_data'] = {
                "email" : user['email'],
                "name" : user['name'],
                "groups" : user['groups'],
                "settings" : user['settings']
            }
    else:
        response['login_success'] = False
    
    return api.build_capsule(response)