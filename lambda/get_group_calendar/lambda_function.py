import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
from bson.objectid import ObjectId
import datetime

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
        recurs = cal['recurring_expenses']
        event_list = []
        for e in events:
            o = {}
            o['creator'] = e['creator']
            o['name'] = e['name']
            o['description'] = e['description']
            o['date'] = e['date']
            o['time'] = e['time']
            o['total'] = None
            o['expense'] = None
            o['frequency'] = 'none'
            o['location'] = e['location']
            o['id'] = e['event_id']
            o['group_id'] = group_id
            event_list.append(o)
        for r in recurs:
            o = {}
            o['creator'] = r['creator']
            o['name'] = r['name']
            o['description'] = r['description']
            o['date'] = r['date']
            o['time'] = r['time']
            o['total'] = r['total']
            o['expense'] = r['expense']
            o['frequency'] = r['frequency']
            o['location'] = None
            o['id'] = r['recurring_expense_id']
            o['group_id'] = group_id
            event_list.append(o)
        response['events'] = event_list
        

    return api.build_capsule(response)
