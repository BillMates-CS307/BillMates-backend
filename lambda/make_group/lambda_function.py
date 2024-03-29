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
                new_cal = {
                    "group_id": group_id,
                    "events": [],
                    "recurring_expenses": []
                }
                cal_id = db['calendars'].insert_one(new_cal).inserted_id
                group_obj = {
                    "name" : payload['name'],
                    "uuid" : group_id,
                    "members" : [payload['manager']],
                    "all_time_members": [payload['manager']],
                    "manager" : payload['manager'],
                    "expenses" : [],
                    "pending_payments": [],
                    "calendar" : cal_id,
                    "shopping list" : [],
                    "settings" : {'fufillment' : 'billmates', 'auto_approve' : False, 'max_char' : 20},
                    "archived" : False,
                    "blacklist" : [],
                    "analytics" : {
                        payload['manager'] : mongo.new_analytics()
                    }
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