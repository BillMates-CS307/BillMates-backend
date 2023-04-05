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
        shop = mongo.query_table("shoppinglists", {'_id' : ObjectId(payload['list_id'])}, db)
        if group == None or shop == None:
            return api.build_capsule(response)
            
        response["get_success"] = True
        response['shopping_list'] = {}
        response['shopping_list']['name'] = shop['name']
        response['shopping_list']['items'] = shop['items']
        response['shopping_list']['isActive'] = shop['isActive']
        response['shopping_list']['_id'] = payload['list_id']

    return api.build_capsule(response)
