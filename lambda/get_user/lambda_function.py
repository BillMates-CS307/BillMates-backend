import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
from bson.objectid import ObjectId

def check_database(data: dict, db) -> bool:
    query = {'email' : data['email']}
    return mongo.query_table('users', query, db)
    
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
        user = check_database(payload, db)
        if user != None:
            response['user'] = {
                'name' : user['name'],
                'groups': user['groups'],
                'settings': user['settings'],
                'attempts' : user['attempts']
             }
        else:
            response['user'] = None

    return api.build_capsule(response)
            