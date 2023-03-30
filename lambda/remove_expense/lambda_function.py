import json
from pymongo import MongoClient
import bundle.g_password
import bundle.mongo as mongo
import bundle.api as api
from bson.objectid import ObjectId
import bundle.notification as notif
import bundle.send as mail
import datetime
    
def lambda_handler(event, context):
       
    # Parameters
    payload = json.loads(event['body'])
    
    # Build reponse JSON
    response = {}

    # Verify token is correct before running more commands
    token = event['headers']['token']
    response["token_success"] = api.check_token(token)
    
    if response["token_success"]:
        db = mongo.get_database()
        expense_id = ObjectId(payload['expense_id'])
        expense = mongo.query_table('expenses', {'_id': expense_id}, db)
        remove = payload['remove']
        if expense != None:
            response['remove_success'] = True
            group = mongo.query_table('groups', {'uuid': expense['group_id']}, db)
            manager = mongo.query_table('users', {'email': group['manager']}, db)
            
            if remove:
                email_users = []
                notif_users = []
                expense['users'].append([expense['owner'], -expense['amount']])
                for u in expense['users']:
                    user = mongo.query_table('users', {'email': u[0]}, db)
                    notif_pref = user['settings']['notification']
                    if notif_pref == 'only email' or notif_pref == 'both':
                        email_users.append(u[0])
                    if notif_pref == 'only billmates' or notif_pref == 'both':
                        notif_users.append(u[0])
                m_name = manager['name']
                body = m_name + ' has removed expense ' + expense['title'] + ' in group ' + \
                    group['name'] + ' which you were a part of.'
                subject = 'Expense removed'
                mail.send_email(subject, body, email_users)
                for u in notif_users:
                    time = str(datetime.datetime.now())
                    notif.make_notification(u, body, time)
                db['expenses'].delete_one({'_id': expense_id})
            else:
                new_val = {'contested': False}
                db['expenses'].update_one({'_id': expense_id}, {'$set': new_val})


    return api.build_capsule(response)