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
        
        new_event = {
            'creator': creator,
            'name': name,
            'description': description,
            'location': location,
            'time': time_string,
            'date': date_string
        }
        
        group = mongo.query_table('groups', {'uuid': group_id}, db)
        email_list = []
        body = creator + ' has created event ' + name + ' on day ' + date_string + ' in group ' + group['name'] + '.'
        subject = 'New event'
        for u in group['members']:
            user = mongo.query_table('users', {'email': u}, db)
            notif_pref = user['settings']['notification']
            if notif_pref == 'only email' or notif_pref == 'both':
                email_list.append(u)
            if notif_pref == 'only billmates' or notif_pref == 'both':
                time = str(datetime.now())
                notif.make_notification(u, body, time)
        mail.send_email(subject, body, email_list)
        
        db['calendars'].update_one({'group_id': group_id}, {'$push': {'events': new_event}})
        
    
    return api.build_capsule(response)