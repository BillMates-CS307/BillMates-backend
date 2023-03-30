import json
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.api as api

def check_database(data: dict, db) -> bool:
    query = {'uuid' : data['uuid']}
    return mongo.query_table('groups', query, db)
    
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
            group = check_database(payload, db)
            groups = db['groups']
            if group != None:
                if not payload['email'] in group['members']:
                    new_arr = list(group['members'])
                    new_arr.append(payload['email'])
                    groups.update_one(group, {"$set": { "members": new_arr} })
                    new_arr = list(group['all_time_members'])
                    new_arr.append(payload['email'])
                    groups.update_one({'uuid': group['uuid']}, {'$set': {'all_time_members': new_arr}})
                    response['group_add_success'] = True
                    
                    # adding group to users group field
                    user = mongo.query_table('users', {'email': payload['email']}, db)
                    if user is None:
                        response['error'] = 'invalid email'
                        api.build_capsule(response)
                        return
                    users = db['users']
                    new_group = payload['uuid']
                    user['groups'].append(new_group)
                    new_val = {'groups': user['groups']}
                    users.update_one({'email': payload['email']}, {'$set': new_val})
                else:
                    response['group_add_success'] = False
            else:
                response = {"ERROR" : "No such group"}
        else:
            response = {"ERROR": "Malformed Body"}
        
    return api.build_capsule(response)