import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
from bson.objectid import ObjectId

def check_database(data: dict) -> dict:
    query = {'email' : data['email']}
    # return mongo.query_user(query, False)
    db = mongo.get_database();
    return mongo.query_table('users', query, db);
    
def lambda_handler(event, context):
       
    # Parameters
    payload = json.loads(event['body'])
    
    # Build reponse JSON
    response = {}

    # Verify token is correct before running more commands
    token = event['headers']['token']
    response["token_success"] = api.check_token(token)
    response['get_success'] = False
    
    if response["token_success"]:
        user = check_database(payload)
        if user != None:
            response['get_success'] = True
            db = mongo.get_database()
            user = mongo.query_table('users', {'email' : payload['email']}, db)
            response['analytics'] = {}
            for uuid in user['groups']:
                group = mongo.query_table('groups', {'uuid' : uuid}, db)
                response['analytics'][group['uuid']] = group['analytics']

    return api.build_capsule(response)
            