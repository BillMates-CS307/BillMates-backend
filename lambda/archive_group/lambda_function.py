import json
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.api as api

def check_database(data: dict, db) -> bool:
    query = {'uuid' : data['group_id']}
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
        if api.check_body(["group_id"], payload):
            db = mongo.get_database()
            if check_database(payload, db):
                db['groups'].update_one({'uuid' : payload['group_id']}, {"$set" : {"archived" : True}})
                response = {"group_archive_success" : True}
            else:
                response = {"group_archive_success" : False}
        else:
            response = {"ERROR": "Malformed Body"}
        
    return api.build_capsule(response)
