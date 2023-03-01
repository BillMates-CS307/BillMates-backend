import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
from bson.objectid import ObjectId

def check_database(data: dict, notifs) -> dict:
    query = {'_id' : ObjectId(data['object_id'])}
    return notifs.find_one(query)

def del_database(data: dict, notifs) -> None:
    query = {'_id' : ObjectId(data['object_id'])}
    notifs.delete_one(query)
    
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
        notifs = db['notifications']
        notif = check_database(payload, notifs)
        response['delete_success'] = notif != None
        if response['delete_success']:
            del_database(payload, notifs)
    
    return api.build_capsule(response)
            
