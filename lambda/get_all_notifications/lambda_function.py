import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
from bson.objectid import ObjectId

def check_database(query: dict, collection) -> bool:
    return collection.find_one(query)
    
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
        users = db['users']
        query_user = {'email' : payload['email']}
        user = check_database(query_user, users)
        notif_arr = user['notifications']
        out_list = []
        for notif in notif_arr:
            info = notifs.find_one({"_id" : ObjectId(notif)})
            my_dict = {
                "_id" : str(info['_id']),
                "sender" : info['sender'],
                "message" : info['message'],
                "time" : str(info['time']),
                "isread" : info['isread']
            }
            out_list.append(my_dict)
        response['notifications'] = out_list
    return api.build_capsule(response)
            
