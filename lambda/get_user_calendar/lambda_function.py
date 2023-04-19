import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
from bson.objectid import ObjectId
import datetime

def lambda_handler(event, context):
    # Parameters
    payload = json.loads(event['body'])
    email = payload['email']
    
    # Build reponse JSON
    response = {}

    # Verify token is correct before running more commands
    token = event['headers']['token']
    response["token_success"] = api.check_token(token)
    response["get_success"] = False
    if response['token_success']:
        db = mongo.get_database()
        user = mongo.query_table("users", {'email' : email}, db)
        if user == None:
            return api.build_capsule(response)
        response['get_success'] = True
        groups = user['groups']
        
        events = []
        recurs = []
        for g in groups:
            cal = db['calendars'].find_one({'group_id': g})
            if cal is None:
                continue
            group_name = mongo.query_table('groups', {'uuid': g}, db)['name']
            for e in cal['events']:
                e['group_name'] = group_name
                e['group_id'] = g
                events.append(e)
            for r in cal['recurring_expenses']:
                r['group_name'] = group_name
                r['group_id'] = g
                recurs.append(r)
        
        event_list = []
        for e in events:
            o = {}
            o['group_name'] = e['group_name']
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
            o['group_id'] = e['group_id']
            event_list.append(o)
        for r in recurs:
            o = {}
            o['group_name'] = e['group_name']
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
            o['group_id'] = r['group_id']
            event_list.append(o)
        response['events'] = event_list
        

    return api.build_capsule(response)
