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
    response["change_success"] = False
    if response['token_success']:
        db = mongo.get_database()
        shop = mongo.query_table("shoppinglists", {'_id' : ObjectId(payload['list_id'])}, db)
        if shop == None:
            return api.build_capsule(response)
            
        response["change_success"] = True
        response['previous_status'] = shop['isActive']
        db['shoppinglists'].update_one({"_id" : ObjectId(payload['list_id'])}, {"$set": {"isActive" : payload['isActive']}})

    return api.build_capsule(response)
