import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
from bson.objectid import ObjectId
    
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
        user = mongo.query_table('users', {'email': payload['email']}, db)
        if user != None:
            response['store_success'] = True
            user['settings']['venmo_token'] = payload['venmo_token']
            new_val = {'settings': user['settings']}
            db['users'].update_one({'email': payload['email']}, {'$set': new_val})
        else:
            response['store_success'] = False

    return api.build_capsule(response)