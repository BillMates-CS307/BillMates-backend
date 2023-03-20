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
    response = {}

    # token verification
    response['token_success'] = api.check_token(token)

    if response['token_success']:
        # retrieving collections
        db = mongo.get_database()

        # retrieving parameters
        parameters = json.loads(event['body'])
        if not api.check_body(['group_id'], parameters):
            response['ERROR'] = 'malformed body'
            return api.build_capsule(response)
        group_id = parameters['group_id']
        
        # group_exists
        group = mongo.query_table('groups', {'uuid': group_id}, db)
        if group is None:
            response['delete_success'] = False
            return api.build_capsule(response)
        response['delete_success'] = True
        
        # getting objects
        users_list = list(db['users'].find())
        g_users = []
        for u in users_list:
            if group_id in u['groups']:
                g_users.append(u['email'])
        
        # send notification to all users
        for us in g_users:
            balance = -69.0
            u = mongo.query_table('users', {'email': us}, db)
            balance = mongo.user_balance_in_group(us, group_id, db)
            notif_pref = u['settings']['notification']
            n_name = mongo.query_table('users', {'email': group['manager']}, db)['name']
            body = n_name + ' has deleted group ' + group['name'] + ' which you are a member of. ' + \
                    'Your outstanding balance in the group was $' + str(balance) + '.'
            if notif_pref == 'only_email' or notif_pref == 'both': # email
                subject = 'Group deleted'
                recipients = [u['email']]
                mail.send_email(subject, body, recipients)
            if notif_pref == 'only_billmates' or notif_pref == 'both': # BillMates notification
                time = str(datetime.datetime.now())
                notif.make_notification(u['email'], body, time)
        
        # delete group from groups:
        db['groups'].delete_one({'uuid': group_id})
        
        
    return api.build_capsule(response)

