import json
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.api as api

def lambda_handler(event, context):
    token = event['headers']['token']
    response = {}

    # token verification
    response['token_success'] = api.check_token(token)

    if response['token_success']:
        db = mongo.get_database()
        # retrieving parameters
        parameters = json.loads(event['body'])
        title = parameters['title'] # title of expense 
        total = parameters['total'] 
        group_id = parameters['group_id'] # group_id for expense
        owner_email = parameters['owner']
        u_expenses = parameters['expense'] # dict of form { 'email_of_user' : amount_owed }
        # notification when due date is reached?
        
        u_expenses[owner_email] = total
        # make sure that total of owed money for each user = total for first user
        check_total = 0
        failure = False
        for u_email in u_expenses:
            # first loop to check that all users are in group and that expense totals add up
            user_groups = mongo.query_table('users', {'email': u_email}, db)['groups']
            
            # if user not in expense's group, return failure
            failure = group_id not in user_groups
            
            if u_expenses[u_email] < 0:
                failure = True
            if not u_email == owner_email: # users who owe money
                check_total += u_expenses[u_email]
        if not check_total == total:
            # if totals are not equal
            failure = True
        if failure:
            response['submit_success'] = False
            return api.build_capsule(response)
        
        temp_expenses = u_expenses.copy()
        
        del u_expenses[owner_email]
        # convert expense dict to array
        users = []
        for u in u_expenses:
            users.append([u, u_expenses[u]])
        # add expense to expense collection
        new_expense = {
            'group_id': group_id,
            'title': title,
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
        for u in temp_expenses:
            u_expense_list = mongo.query_table('users', {'email': u}, db)['expenses']
            u_expense_list.append(insert_result.inserted_id)
            new_val = {'expenses': u_expense_list}
            db['users'].update_one({'email': u}, {'$set': new_val})
        
        response['submit_success'] = True
    return api.build_capsule(response)
