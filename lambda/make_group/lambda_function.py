import json
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.api as api
import uuid as uu

cal_template = {
    "january": [],
    "february": [],
    "march": [],
    "april": [],
    "june": [],
    "july": [],
    "august": [],
    "september": [],
    "october": [],
    "november": [],
    "december": [],
    "group_name": ""
}

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
                cal_template['group_name'] = payload['name']
                groups = db['groups']
                group_id = str(uu.uuid4())
                group_obj = {
                    "name" : payload['name'],
                    "uuid" : group_id,
                    "members" : [payload['manager']],
                    "all_time_members": [payload['manager']],
                    "manager" : payload['manager'],
                    "expenses" : [],
                    "pending_payments": [],
                    "calendar" : db['calendars'].insert_one(cal_template).inserted_id,
                    "shopping list" : [],
                    "settings" : {'fufillment' : 'billmates', 'auto_approve' : False, 'max_char' : 20},
                    "archived" : False,
                    "blacklist" : []
                }
                groups.insert_one(group_obj)
                response['make_group_success'] = True
                
                # add group to manager's groups field
                db['users'].update_one({'email' : payload['manager']}, {"$push": {"groups" : str(group_id)}})
                
            else:
                response['make_group_success'] = False
        else: 
            response = {"ERROR": "Malformed Body"}
        
    return api.build_capsule(response)