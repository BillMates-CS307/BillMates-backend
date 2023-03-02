import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
from bson.objectid import ObjectId

def check_database(data: dict, notifs) -> bool:
    query = {'_id' : ObjectId(data['object_id'])}
    return notifs.find_one(query)
    
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
        if notif != None:
            notifs.update_one(notif, {"$set" : {"isread": True}})
            response['read_success'] = True
        else:
            response['read_success'] = False
    
    return api.build_capsule(response)
            
