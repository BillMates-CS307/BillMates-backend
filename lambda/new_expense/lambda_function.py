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
        db = mongo.get_database()
        # retrieving parameters
        parameters = {}
        try:
            parameters = json.loads(event['body'])
        except:
            parameters = event['body']
        title = parameters['title'] # title of expense 
        total = parameters['total'] 
        comment = parameters['comment']
        group_id = parameters['group_id'] # group_id for expense
        owner_email = parameters['owner']
        u_expenses = parameters['expense'] # dict of form { 'email_of_user' : amount_owed }
        tag = parameters['tag']
        # notification when due date is reached?
        
        if total < 0:
            response['submit_success'] = False
            return api.build_capsule(response)
        
        # convert expense dict to array
        users = []
        for u in u_expenses:
            users.append([u, u_expenses[u]])
        # add expense to expense collection
        new_expense = {
            'group_id': group_id,
            'title': title,
            'comment': comment,
            'tag' : tag,
            'owner': owner_email,
            'users': users,
            'amount': total,
            'is_payout': False,
            'contested': False
        }
        insert_result = db['expenses'].insert_one(new_expense)
        
        # add expense to group expenses field
        g_expenses = mongo.query_table('groups', {'uuid': group_id}, db)['expenses']
        g_expenses.append(insert_result.inserted_id)
        new_val = {'expenses': g_expenses}
        db['groups'].update_one({'uuid': group_id}, {'$set': new_val})
        
        # add expense to users expense fields
        temp_expenses = u_expenses.copy()
        temp_expenses[owner_email] = -total
        for u in temp_expenses:
            u_expense_list = mongo.query_table('users', {'email': u}, db)['expenses']
            u_expense_list.append(insert_result.inserted_id)
            new_val = {'expenses': u_expense_list}
            db['users'].update_one({'email': u}, {'$set': new_val})
        
        # notify users on expense
        email_users = []
        notif_users = []
        for u in u_expenses:
            user = mongo.query_table('users', {'email': u}, db)
            notif_pref = user['settings']['notification']
            if notif_pref == 'only email' or notif_pref == 'both':
                email_users.append(u)
            if notif_pref == 'only billmates' or notif_pref == 'both':
                notif_users.append(u)
        o_name = mongo.query_table('users', {'email': owner_email}, db)['name']
        g_name = mongo.query_table('groups', {'uuid': group_id}, db)['name']
        body = o_name + ' has created expense ' + title + ' in group ' + \
            g_name + '. You are being charged $' + str(u_expenses[u]) + '.'
        subject = 'New Expense'
        mail.send_email(subject, body, email_users)
        for u in notif_users:
            time = str(datetime.datetime.now())
            notif.make_notification(u, body, time)
        
        
        response['submit_success'] = True
    return api.build_capsule(response)
