import json
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.api as api

def check_database(data: dict, groups) -> bool:
    query = {'uuid' : data['uuid']}
    return groups.find_one(query)
    
def lambda_handler(event, context):
    # Parameters
    payload = json.loads(event['body'])
    
    # Build reponse JSON
    response = {}

    # Verify token is correct before running more commands
    token = event['headers']['token']
    response["token_success"] = api.check_token(token)
    
    if response["token_success"]:
        if api.check_body(["email", "uuid"], payload):
            db = mongo.get_database()
            groups = db['groups']
            group = check_database(payload, groups)
            if group != None:
                if not payload['email'] in group['members']:
                    new_arr = list(group['members'])
                    new_arr.append(payload['email'])
                    groups.update_one(group, {"$set": { "members": new_arr} })
                    response['group_add_success'] = True
                    
                    # adding group to users group field
                    users = db['users']
                    user_groups = users.find_one({'email': payload['email']})['groups']
                    new_group = {}
                    new_group['group_id'] = payload['uuid']
                    new_group['name'] = group['name']
                    new_group['balance'] = 0
                    user_groups.append(new_group)
                    new_val = {'groups': user_groups}
                    users.update_one({'email': payload['email']}, {'$set': new_val})
                else:
                    response['group_add_success'] = False
            else:
                response = {"ERROR" : "No such group"}
        else:
            response = {"ERROR": "Malformed Body"}
        
    return api.build_capsule(response)