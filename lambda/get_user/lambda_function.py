import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
from bson.objectid import ObjectId

def check_database(data: dict) -> dict:
    query = {'email' : data['email']}
    # return mongo.query_user(query, False)
    db = mongo.get_database();
    return mongo.query_table('users', query, db);
    
def lambda_handler(event, context):
       
    # Parameters
    payload = json.loads(event['body'])
    
    # Build reponse JSON
    response = {}

    # Verify token is correct before running more commands
    token = event['headers']['token']
    response["token_success"] = api.check_token(token)
    
    if response["token_success"]:
        user = check_database(payload)
        if user != None:
            new_groups = []
            db = mongo.get_database()
            for group_id in user['groups']:
                group = mongo.query_table('groups', {'uuid' : group_id}, db)
                build = {}
                build['uuid'] = group_id
                build['name'] = mongo.get_group_name(group_id, db)
                build['balance'] = mongo.user_balance_in_group(user['email'], group_id, db)
                build['archived'] = group['archived']
                new_groups.append(build)
            response['user'] = {
                'name' : user['name'],
                'groups': list(new_groups),
                'settings': user['settings'],
                'attempts' : user['attempts']
             }

    return api.build_capsule(response)
            