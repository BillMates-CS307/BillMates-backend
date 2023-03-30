import json
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.g_password
import bundle.api as api
import bundle.send as mail
import bundle.notification as notif
from bson.objectid import ObjectId
import datetime

def lambda_handler(event, context):
    
    payload = json.loads(event['body'])
    token = event['headers']['token']
    response = {}

    # token verification
    response['token_success'] = api.check_token(token)
    if response['token_success']:
        db = mongo.get_database()
        email = payload['email']
        group_id = payload['group_id']
        user = mongo.query_table('users', {'email': email}, db)
        group = mongo.query_table('groups', {'uuid': group_id}, db)
        if user is None or group is None:
            response['delete_success'] = False
            return api.build_capsule(response)
        response['delete_success'] = True
        group['members'].remove(email)
        user['groups'].remove(group_id)
        db['groups'].update_one({'uuid': group_id}, {'$set': {'members': group['members']}})
        db['users'].update_one({'email': email}, {'$set': {'groups': user['groups']}})
        
        # send notification
        notif_pref = user['settings']['notification']
        m_name = mongo.query_table('users', {'email': group['manager']}, db)['name']
        body = m_name + ' has kicked you from group ' + group['name']
        if notif_pref == 'only email' or notif_pref == 'both': # email
            subject = 'Kicked from group'
            recipients = [email]
            mail.send_email(subject, body, recipients)
        if notif_pref == 'only billmates' or notif_pref == 'both': # BillMates notification
            time = str(datetime.datetime.now())
            notif.make_notification(email, body, time)
        
    return api.build_capsule(response)
