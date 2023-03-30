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
    token = event['headers']['token']
    response = {}

    # token verification
    response['token_success'] = api.check_token(token)

    if response['token_success']:
        # retrieving collections
        db = mongo.get_database()
        pending_expenses = db['pending_paid_expenses']

        # retrieving parameters
        parameters = json.loads(event['body'])
        email = parameters['email']
        expense_id = ObjectId(parameters['expense_id'])
        amount = parameters['amount']
        
        # check if expense exists
        expense = mongo.query_table('expenses', {'_id': expense_id}, db)
        if expense is None:
            response['pay_success'] = False
            return api.build_capsule(response)
        response['pay_success'] = True
        
        # getting objects
        group_id = expense['group_id']
        group = mongo.query_table('groups', {'uuid': group_id}, db)
        user = mongo.query_table('users', {'email': email}, db)
        owner = mongo.query_table('users', {'email': expense['owner']}, db)
        expenses = db['expenses']
        users = db['users']
        groups = db['groups']
        user_index = -1
        for i in range(0, len(expense['users']) - 1):
            if expense['users'][i][0] == email:
                user_index = i
        
        # update/delete expense
        if amount < expense['users'][user_index][1]: # if the expense is not being paid in full
            # update amount and users amount owed fields
            expense['users'][user_index][1] -= amount
            expense['amount'] -= amount
            new_val = {'users': expense['users']}
            expenses.update_one({'_id': expense_id}, {'$set': new_val})
            new_val = {'amount': expense['amount']}
            expenses.update_one({'_id': expense_id}, {'$set': new_val})
        else: # if the expense is being paid in full
            # remove user from users field of expense
            expense['users'].pop(user_index)
            new_val = {'users': expense['users']}
            expenses.update_one({'_id': expense_id}, {'$set': new_val})
            # if user is only debtor on expense, remove expense
            if len(expense['users']) == 0:
                expenses.delete_one({'_id': expense_id})
                
        # create entry in pending_paid_expenses
        pending_expense = {
            'expense_id': expense_id,
            'group_id': group_id,
            'title': expense['title'],
            'comment': expense['comment'],
            'amount_paid': amount,
            'paid_by': email,
            'paid_to': owner['email']
        }
        payment_id = pending_expenses.insert_one(pending_expense).inserted_id
        group_pending = mongo.query_table('groups', {'uuid': group_id}, db)['pending_payments']
        group_pending.append(payment_id)
        new_val = {'pending_payments': group_pending}
        db['groups'].update_one({'uuid': group_id}, {'$set': new_val})
        
        # send owner notification
        notif_pref = mongo.query_table('users', {'email': owner['email']}, db)['settings']['notification']
        n_name = mongo.query_table('users', {'email': email}, db)['name']
        body = n_name + ' has paid $' + str(amount) + ' of your expense request ' + \
                expense['title'] + ' in group ' + group['name'] + '.'
        if notif_pref == 'only email' or notif_pref == 'both': # email
            subject = 'Payment rec'
            recipients = [owner['email']]
            mail.send_email(subject, body, recipients)
        if notif_pref == 'only billmates' or notif_pref == 'both': # BillMates notification
            time = str(datetime.datetime.now())
            notif.make_notification(owner['email'], body, time)
            
        
    return api.build_capsule(response)