import json
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.api as api

def lambda_handler(event, context):
    token = event['headers']['token']
    response = {}

    # token verification
    response['token_success'] = api.check_token(token)

    if response['token_success']:
        db = mongo.get_database()

        # retrieving parameters
        parameters = json.loads(event['body'])
        email = parameters['email']
        password = parameters['password']
        name = parameters['name']
        
        users = db['users']
        user = mongo.query_user({'email': email})
        response['signup_success'] = user == None
        if response['signup_success']:
            new_user = {
                'email': email,
                'password': password,
                'groups': [],
                'name': name,
                'settings': {'notification': 'both'},
                'attempts': 0
            }
            users.insert_one(new_user)
    else:
        response['signup_success'] = False
    
    return api.build_capsule(response)