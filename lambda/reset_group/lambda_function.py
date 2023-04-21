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
        group_id = payload['group_id']
        group = mongo.query_table('groups', {'uuid': group_id}, db)
        if group is None:
            response['reset_success'] = False
            return api.build_capsule(response)
        response['reset_success'] = True
        
        expense_list = []
        payment_list = []
        shop_list = []
        for e in group['expenses']:
            expense_list.append(e)
        for p in group['pending_payments']:
            payment_list.append(p)
        for s in group['shopping list']:
            shop_list.append(s)
        db['expenses'].delete_many({'_id': {'$in': expense_list}})
        db['pending_paid_expenses'].delete_many({'_id': {'$in': payment_list}})
        db['shoppinglists'].delete_many({'_id': {'$in': shop_list}})
        group['shopping list'] = []
        db['groups'].update_one({'uuid' : group['uuid']}, {'$set':{'shopping list' : group['shopping list']}})
        # send notification
        email_users = []
        m_name = mongo.query_table('users', {'email': group['manager']}, db)['name']
        body = m_name + ' has reset group ' + group['name'] + '. All expenses and payments have been deleted and balances set to 0.'
        for u in group['members']:
            user = mongo.query_table('users', {'email': u}, db)
            notif_pref = user['settings']['notification']
            if notif_pref == 'only email' or notif_pref == 'both': # email
                email_users.append(u);
            if notif_pref == 'only billmates' or notif_pref == 'both': # BillMates notification
                time = str(datetime.datetime.now())
                notif.make_notification(u, body, time) 
        recipients = email_users
        subject = 'Group reset'
        mail.send_email(subject, body, recipients)
        
        
    return api.build_capsule(response)
