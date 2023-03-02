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
        expenses = db['expenses']
        users = db['users']
        groups = db['groups']
        pending_expenses = db['pending_paid_expenses']

        # retrieving parameters
        parameters = json.loads(event['body'])
        if not api.check_body(['accepted', 'expense_id'], parameters):
            response['ERROR'] = 'malformed body'
            return api.build_capsule(response)
        status = parameters['accepted'] # true means accepted, false means denied
        original_id = ObjectId(parameters['expense_id']) # convert from string
        
        # payment_id is valid
        if pending_expenses.find_one({'expense_id': original_id}) is None:
            response['handle_success'] = False
            return api.build_capsule(response)
        response['handle_success'] = True
        
        # getting objects
        pending = pending_expenses.find_one({'expense_id': original_id})
        payment_id = pending['_id']
        group_id = pending['group_id']
        group = groups.find_one({'uuid': group_id})
        paid_to = pending['paid_to']
        paid_by = pending['paid_by']
        amount = pending['amount_paid']
        title = pending['title']
        
        # is payment accepted (status == true) means accepted
        if not status: # payment denied
        
            # send notification to paid_by
            notif_pref = users.find_one({'email': paid_by})['settings']['notification']
            body = paid_to + ' has denied your payment of $' + str(amount) + ' for ' + \
                        title + ' in group ' + group['name'] + '.'
            if notif_pref == 'only_email' or notif_pref == 'both': # email
                subject = 'Payment denied'
                recipients = [paid_by]
                mail.send_email(subject, body, recipients)
            if notif_pref == 'only_billmates' or notif_pref == 'both': # BillMates notification
                time = str(datetime.datetime.now())
                notif.make_notification(paid_by, body, time)
            
            # update user balances
            u_paid_by = users.find_one({'email': paid_by})
            u_paid_to = users.find_one({'email': paid_to})
            for g in u_paid_by['groups']:
                if g['group_id'] == group_id:
                    g['balance'] -= amount
            for g in u_paid_to['groups']:
                if g['group_id'] == group_id:
                    g['balance'] += amount
            new_val_b = {'groups': u_paid_by['groups']}
            new_val_t = {'groups': u_paid_to['groups']}
            users.update_one({'email': paid_by}, {'$set': new_val_b})
            users.update_one({'email': paid_to}, {'$set': new_val_t})
            
            # check if expense still exists, if not create it again, add to expenses collection and to group
            og_expense = expenses.find_one({'_id': original_id})
            if og_expense is None:
                new_expense = {
                    '_id': original_id,
                    'title': title,
                    'group_id': group_id,
                    'users': {paid_by: amount},
                    'amount': amount,
                    'owner': paid_to
                }
                expenses.insert_one(new_expense)
                group['expenses'].append(original_id)
                new_val = {'expenses': group['expenses']}
                groups.update_one({'uuid': group_id}, {'$set': new_val})
            else: # if expense still exists, check if user still owes on it, if not add user entry to expenses
                if og_expense['users'][paid_by] is None: # user paid in full
                    og_expense['users'][paid_by] = amount
                else: # user paid in part
                    og_expense['users'][paid_by] += amount
                new_val = {'users': og_expense['users']}
                expenses.update_one({'_id': original_id}, {'$set': new_val})
            
        # remove pending payment
        pending_expenses.delete_one({'_id': payment_id})
        
    return api.build_capsule(response)
