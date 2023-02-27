import json
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.api as api
import uuid as uu

def check_database(data: dict, groups) -> bool:
    query = {'manager':data['manager'], 'name' : data['name']}
    return groups.find_one(query) != None
    
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
            groups = db['groups']
            if not check_database(payload, groups):
                group_obj = {
                    "name" : payload['name'],
                    "uuid" : str(uu.uuid4()),
                    "members" : [],
                    "manager" : payload['manager'],
                    "expenses" : [],
                    "calendar" : [],
                    "shopping list" : []
                }
                groups.insert_one(group_obj)
                response['make_group_success'] = True
            else:
                response['make_group_success'] = False
        else: 
            response = {"ERROR": "Malformed Body"}
        
    return api.build_capsule(response)