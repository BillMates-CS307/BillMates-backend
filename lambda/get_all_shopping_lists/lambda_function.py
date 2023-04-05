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
    response["get_success"] = response["token_success"]
    if response['token_success']:
        db = mongo.get_database()
        group = mongo.query_table("groups", {'uuid' : payload['group_id']}, db)
        response['shopping_lists'] = []
        for obj_id in group['shopping list']:
            shop = mongo.query_table("shoppinglists", {'_id' : obj_id}, db)
            response['shopping_lists'].append({})
            response['shopping_lists'][~0]['name'] = shop['name']
            response['shopping_lists'][~0]['items'] = shop['items']
            response['shopping_lists'][~0]['isActive'] = shop['isActive']
    
    return api.build_capsule(response)
