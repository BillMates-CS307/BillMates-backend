import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
from bson.objectid import ObjectId

def check_database(data: dict, db) -> bool:
    query = {'_id' : ObjectId(data['object_id'])}
    return mongo.query_table('notifications', query, db)
    
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
        notif = check_database(payload, db)
        if notif != None:
            response['notification'] = {
                'id': payload['object_id'],
                'user': notif['user'],
                'sender': notif['sender'],
                'message': notif['message'],
                'time': str(notif['time']),
                'isread': notif['isread']
             }
        else:
            response['notification'] = None
    
    return api.build_capsule(response)
            
