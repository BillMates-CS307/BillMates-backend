import json
from pymongo import MongoClient
import bundle.g_password
import bundle.mongo as mongo
import bundle.api as api
from bson.objectid import ObjectId
import bundle.send as mail
import bundle.notification as notif
import datetime

def lambda_handler(event, context):
    token = event['headers']['token']
    payload = json.loads(event['body'])
    response = {}
    
    # token verification
    response['token_success'] = api.check_token(token)
    
    if response['token_success']:
        db = mongo.get_database()
        event_id = payload['event_id']
        group_id = payload['group_id']
        cal = mongo.query_table('calendars', {'group_id': group_id}, db)
        if cal is None:
            response['remove_success'] = False
            return api.build_capsule(response)
        events = cal['events']
        event = {}
        for e in events:
            if e['event_id'] == event_id:
                event = e
        if event == {}:
            response['remove_success'] = False
            return api.build_capsule(response)
        events.remove(event)
        db['calendars'].update_one({'group_id': group_id}, {'$set': {'events': events}})
        response['remove_success'] = True
        
    return api.build_capsule(response)
