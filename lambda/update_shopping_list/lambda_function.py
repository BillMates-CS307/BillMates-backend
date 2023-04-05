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
        name = payload['item_name']
        if shop == None or not shop['isActive']:
            return api.build_capsule(response)
        response["change_success"] = True
        items = shop['items']
        if name not in items and payload['remove_item'] or name in items and not payload['remove_item']:
            return api.build_capsule(response)
        if payload['remove_item']:
            items.remove(name)
        else:
            items.append(name)
        db['shoppinglists'].update_one({'_id' : ObjectId(payload['list_id'])}, {'$set' : {'items' : items}})
        
    return api.build_capsule(response)
