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
    response["get_success"] = False
    if response['token_success']:
        db = mongo.get_database()
        group = mongo.query_table("groups", {'uuid' : payload['group_id']}, db)
        if group == None:
            return api.build_capsule(response)
            
        response['get_success'] = True
        response['group_calendar'] = db['calendars'].find_one({'_id' : group['calendar']})
        del response['group_calendar']['_id']

    return api.build_capsule(response)