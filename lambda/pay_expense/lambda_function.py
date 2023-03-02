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
        expenses = db['expenses']
        users = db['users']
        groups = db['groups']
        pending_expenses = db['pending_paid_expenses']

        # retrieving parameters
        parameters = json.loads(event['body'])
        email = parameters['email']
        expense_id = ObjectId(parameters['expense_id'])
        amount = parameters['amount']
        
        # getting objects
        expense = expenses.find_one({'_id': expense_id})
        group_id = expense['group_id']
        group = groups.find_one({'uuid': group_id})
        user = users.find_one({'email': email})
        owner = users.find_one({'email': expense['owner']})
        
        
        # check if amount is greater than amount owed
        if amount > expense['users'][email]:
            response['pay_success'] = False
            return api.build_capsule(response)
        response['pay_success'] = True
        
        # update users balances
        for g in user['groups']:
            if g['group_id'] == group_id:
                g['balance'] += amount
        for g in owner['groups']:
            if g['group_id'] == group_id:
                g['balance'] -= amount
        new_val_u = {'groups': user['groups']}
        new_val_o = {'groups': owner['groups']}
        users.update_one({'email': email}, {'$set': new_val_u})
        users.update_one({'email': expense['owner']}, {'$set': new_val_o})
        
        # update/delete expense
        if amount < expense['users'][email]: # if the expense is not being paid in full
            # update amount and users amount owed fields
            expense['users'][email] -= amount
            expense['amount'] -= amount
            new_val = {'users': expense['users']}
            expenses.update_one({'_id': expense_id}, {'$set': new_val})
            new_val = {'amount': expense['amount']}
            expenses.update_one({'_id': expense_id}, {'$set': new_val})
        else: # if the expense is being paid in full
            # remove user from users field of expense
            del expense['users'][email]
            new_val = {'users': expense['users']}
            expenses.update_one({'_id': expense_id}, {'$set': new_val})
            # if user is only debtor on expense, remove expense
            if len(expense['users']) == 0:
                # from expenses
                expenses.delete_one({'_id': expense_id})
                # from group
                temp_exps = []
                for e in group['expenses']:
                    if not expense_id == e:
                        temp_exps.append(e)
                new_val = {'expenses': temp_exps}
                groups.update_one({'uuid': group_id}, {'$set': new_val})
                
        # create entry in pending_paid_expenses
        pending_expense = {
            'expense_id': expense_id,
            'group_id': group_id,
            'title': expense['title'],
            'amount_paid': amount,
            'paid_by': email,
            'paid_to': owner['email']
        }
        pending_expenses.insert_one(pending_expense)
        
        # send owner notification
        notif_pref = users.find_one({'email': owner['email']})['settings']['notification']
        body = email + ' has paid $' + str(amount) + ' of your expense request ' + \
                expense['title'] + ' in group ' + group['name'] + '.'
        if notif_pref == 'only_email' or notif_pref == 'both': # email
            subject = 'Payment rec'
            recipients = [owner['email']]
            mail.send_email(subject, body, recipients)
        if notif_pref == 'only_billmates' or notif_pref == 'both': # BillMates notification
            time = str(datetime.datetime.now())
            notif.make_notification(owner['email'], body, time)
            
        
    return api.build_capsule(response)