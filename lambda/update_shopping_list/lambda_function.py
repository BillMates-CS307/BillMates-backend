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
        if shop == None or not shop['isActive']:
            return api.build_capsule(response)
        response["change_success"] = True
        idx = -1
        items = shop['items']
        for i in range(len(items)):
            if items[i]['name'] == payload['item_name']:
                idx = i
                break
        if idx == -1 and payload['remove_item'] or idx != -1 and not payload['remove_item']:
            return api.build_capsule(response)
        if payload['remove_item']:
            items.pop(idx)
        else:
            items.append({'name': payload['item_name'], 'cost':0, 'quantity':0})
        db['shoppinglists'].update_one({'_id' : ObjectId(payload['list_id'])}, {'$set' : {'items' : items}})
        
    return api.build_capsule(response)
