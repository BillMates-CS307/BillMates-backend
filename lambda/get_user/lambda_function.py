import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
from bson.objectid import ObjectId

def check_database(data: dict, users) -> bool:
    query = {'email' : data['email']}
    return users.find_one(query)
    
def lambda_handler(event, context):
       
    # Parameters
    payload = json.loads(event['body'])
    
    # Build reponse JSON
    response = {}

    # Verify token is correct before running more commands
    token = event['headers']['token']
    response["token_success"] = api.check_token(token)
    
    if response["token_success"]:
        db = mongo.get_database()
        users = db['users']
        user = check_database(payload, users)
        if user != None:
            response['user'] = {
                'sender': user['email'],
                'groups': user['groups'],
                'settings': user['settings'],
                'attempts' : user['attempts']
             }
        else:
            response['user'] = None
    
    return api.build_capsule(response)
            
