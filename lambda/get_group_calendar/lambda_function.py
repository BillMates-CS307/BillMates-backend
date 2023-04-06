import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
from bson.objectid import ObjectId

def lambda_handler(event, context):
    # Parameters
    payload = json.loads(event['body'])
    group_id = payload['group_id']
    
    # Build reponse JSON
    response = {}

    # Verify token is correct before running more commands
    token = event['headers']['token']
    response["token_success"] = api.check_token(token)
    response["get_success"] = False
    if response['token_success']:
        db = mongo.get_database()
        group = mongo.query_table("groups", {'uuid' : group_id}, db)
        if group == None:
            return api.build_capsule(response)
            
        response['get_success'] = True
        cal = db['calendars'].find_one({'group_id': group_id})
        events = cal['events']
        # recurs = cal['recurring_expenses']
        # not going to add recurring expenses yet
        event_list = []
        for e in events:
            event_list.append(e)
            # modification of events will have to happen when we start including recurring expenses
        response['events'] = event_list
        

    return api.build_capsule(response)
