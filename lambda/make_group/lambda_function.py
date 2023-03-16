import json
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.api as api
import uuid as uu

def check_database(data: dict, db) -> bool:
    query = {'manager':data['manager'], 'name' : data['name']}
    return mongo.query_table('groups', query, db) != None
    
def lambda_handler(event, context):
    # Parameters
    payload = json.loads(event['body'])
    
    # Build reponse JSON
    response = {}

    # Verify token is correct before running more commands
    token = event['headers']['token']
    response["token_success"] = api.check_token(token)
    
    if response['token_success']:
        if api.check_body(["name", "manager"], payload):
            db = mongo.get_database()
            if not check_database(payload, db):
                groups = db['groups']
                group_id = str(uu.uuid4())
                group_obj = {
                    "name" : payload['name'],
                    "uuid" : group_id,
                    "members" : [payload['manager']],
                    "manager" : payload['manager'],
                    "expenses" : [],
                    "pending_payments": [],
                    "calendar" : [],
                    "shopping list" : []
                }
                groups.insert_one(group_obj)
                response['make_group_success'] = True
                
                # add group to manager's groups field
                manager = mongo.query_table('users', {'email': payload['manager']}, db)
                users = db['users']
                manager['groups'].append(group_id)
                new_val = {'groups': manager['groups']}
                users.update_one({'email': payload['manager']}, {'$set': new_val})
            else:
                response['make_group_success'] = False
        else: 
            response = {"ERROR": "Malformed Body"}
        
    return api.build_capsule(response)