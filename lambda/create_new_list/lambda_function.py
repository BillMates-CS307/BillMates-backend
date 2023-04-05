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
    response["create_success"] = False
    if response['token_success']:
        db = mongo.get_database()
        group = mongo.query_table("groups", {'uuid' : payload['group_id']}, db)
        if group != None:
            for obj_id in group['shopping list']:
                shop = mongo.query_table("shoppinglists", {'_id' : obj_id}, db)
                if payload['name'] == shop['name']:
                    return api.build_capsule(response)
            response["create_success"] = True
            new_list = {'name' : payload['name'], 'items' : [], 'isActive' : True}
            _id = db['shoppinglists'].insert_one(new_list)
            db['groups'].update_one({'uuid' : payload['group_id']}, {'$push' : {'shopping list' : _id.inserted_id}})

        
    return api.build_capsule(response)
