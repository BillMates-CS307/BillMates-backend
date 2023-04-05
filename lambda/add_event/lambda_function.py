import json
from pymongo import MongoClient
import bundle.g_password
import bundle.mongo as mongo
import bundle.api as api
from bson.objectid import ObjectId
import bundle.notification as notif
import bundle.send as mail
import datetime
from datetime import datetime

def lambda_handler(event, context):
    token = event['headers']['token']
    response = {}

    # token verification
    response['token_success'] = api.check_token(token)

    if response['token_success']:
        db = mongo.get_database()

        # retrieving parameters
        parameters = json.loads(event['body'])
        group_id = parameters['group_id']
        creator = parameters['email']
        name = parameters['name']
        description = parameters['description']
        location = parameters['location']
        date_string = parameters['date']
        time_string = parameters['time']
        
        response['add_success'] = True
        e_time = datetime.fromisoformat(date_string + 'T' + time_string)
        
        new_event = {
            'creator': creator,
            'name': name,
            'description': description,
            'location': location,
            'time': str(e_time)
        }
        
        # add notifications
        
        db['calendars'].update_one({'group_id': group_id}, {'$push': {'events': new_event}})
        
    
    return api.build_capsule(response)