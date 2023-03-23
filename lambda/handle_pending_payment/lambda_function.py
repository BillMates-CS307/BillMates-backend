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
    token = event['headers']['token']
    response = {}

    # token verification
    response['token_success'] = api.check_token(token)

    if response['token_success']:
        # retrieving collections
        db = mongo.get_database()

        # retrieving parameters
        parameters = json.loads(event['body'])
        if not api.check_body(['accepted', 'payment_id'], parameters):
            response['ERROR'] = 'malformed body'
            return api.build_capsule(response)
        status = parameters['accepted'] # true means accepted, false means denied
        payment_id = ObjectId(parameters['payment_id']) # convert from string
        
        p = "pending_paid_expenses"
        payment = mongo.query_table(p, {'_id': payment_id}, db)
        # payment_id is valid
        if payment is None:
            response['handle_success'] = False
            return api.build_capsule(response)
        response['handle_success'] = True
        
        # getting objects
        original_id = payment['expense_id']
        original = mongo.query_table('expenses', {'_id': original_id}, db)
        group_id = payment['group_id']
        group = mongo.query_table('groups', {'uuid': group_id}, db)
        paid_to = payment['paid_to']
        paid_by = payment['paid_by']
        amount = payment['amount_paid']
        title = payment['title']
        
        # is payment accepted (status == true) means accepted
        if not status: # payment denied
        
            # send notification to paid_by
            notif_pref = mongo.query_table('users', {'email': paid_by}, db)['settings']['notification']
            n_name = mongo.query_table('users', {'email': paid_to}, db)['name']
            body = n_name + ' has denied your payment of $' + str(amount) + ' for ' + \
                        title + ' in group ' + group['name'] + '.'
            if notif_pref == 'only_email' or notif_pref == 'both': # email
                subject = 'Payment denied'
                recipients = [paid_by]
                mail.send_email(subject, body, recipients)
            if notif_pref == 'only_billmates' or notif_pref == 'both': # BillMates notification
                time = str(datetime.datetime.now())
                notif.make_notification(paid_by, body, time)
            
            # check if expense still exists, if not create it again, add to expenses collection and to group
            if original is None:
                new_expense = {
                    '_id': original_id,
                    'title': title,
                    'group_id': group_id,
                    'users': [(paid_by, amount)],
                    'amount': amount,
                    'owner': paid_to
                }
                db['expenses'].insert_one(new_expense)
                group['expenses'].append(original_id)
                owner = mongo.query_table('users', {'email': paid_to}, db)
                debtor = mongo.query_table('users', {'email': paid_by}, db)
                owner['expenses'].append(original_id)
                debtor['expenses'].append(original_id)
                new_valg = {'expenses': group['expenses']}
                new_valo = {'expenses': owner['expenses']}
                new_vald = {'expenses': debtor['expenses']}
                db['groups'].update_one({'uuid': group_id}, {'$set': new_valg})
                db['users'].update_one({'email': paid_to}, {'$set': new_valo})
                db['users'].update_one({'email': paid_by}, {'$set': new_vald})
            else: # if expense still exists, check if user still owes on it, if not add user entry to expenses
                in_full = True
                for u in original['users']:
                    if u[0] == paid_by: # user paid in part
                        in_full = False
                        u[1] += amount
                if in_full: # user paid in full
                    original['users'].append((paid_by, amount))
                new_val = {'users': original['users']}
                db['expenses'].update_one({'_id': original_id}, {'$set': new_val})
            
        # remove pending payment
        db[p].delete_one({'_id': payment_id})
        
    return api.build_capsule(response)