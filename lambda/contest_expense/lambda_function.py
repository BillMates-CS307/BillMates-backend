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
        user = mongo.query_table('users', {'email': payload['email']}, db)
        expense_id = ObjectId(payload['expense_id'])
        expense = mongo.query_table('expenses', {'_id': expense_id}, db)
        if user != None and expense != None:
            response['contest_success'] = True
            group = mongo.query_table('groups', {'uuid': expense['group_id']}, db)
            manager = mongo.query_table('users', {'email': group['manager']}, db)
            
            new_val = {'contested': True}
            db['expenses'].update_one({'_id': expense_id}, {'$set': new_val})
            
            notif_pref = manager['settings']['notification']
            n_name = user['name']
            body = n_name + ' has contested expense ' + expense['title'] + ' in group ' + \
                    group['name'] + '.'
            if notif_pref == 'only email' or notif_pref == 'both': # email
                subject = 'Expense contested in your BillMates group'
                recipients = [manager['email']]
                mail.send_email(subject, body, recipients)
            if notif_pref == 'only billmates' or notif_pref == 'both': # BillMates notification
                time = str(datetime.datetime.now())
                notif.make_notification(manager['email'], body, time)
        else:
            response['contest_success'] = False

    return api.build_capsule(response)