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
        users = db['users']
        expenses = db['expenses']
        groups = db['groups']
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
            user_groups = users.find_one({'email': u_email})['groups']
            
            # if user not in expense's group, return failure
            failure = True
            for g in user_groups: 
                if g['group_id'] == group_id:
                    failure = False
            
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
        for u_email in u_expenses:
            # loop to update group balance of each user
            user_groups = users.find_one({'email': u_email})['groups']
            expense_group = {} # group which the expense is in
            for g in user_groups:
                if g['group_id'] == group_id:
                    expense_group = g
               
            # update balance of expense_group     
            if u_email == owner_email: # user who submitted expense
                expense_group['balance'] += u_expenses[u_email]
            else: # users who owe money
                expense_group['balance'] -= u_expenses[u_email]
            
            for g in user_groups: # update correct group in user_groups 
                if g['group_id'] == group_id:
                    g = expense_group
                    
            new_val = {'groups' : user_groups}
            users.update_one({'email': u_email}, {'$set': new_val})
            # send notification?
        
        del u_expenses[owner_email]
        # add expense to expense collection
        new_expense = {
            'group_id': group_id,
            'title': title,
            'owner': owner_email,
            'users': u_expenses,
            'amount': total
        }
        insert_result = expenses.insert_one(new_expense)
        
        # add expense to group expenses field
        g_expenses = groups.find_one({'uuid': group_id})['expenses']
        g_expenses.append(insert_result.inserted_id)
        new_val = {'expenses': g_expenses}
        groups.update_one({'uuid': group_id}, {'$set': new_val})
        
        response['submit_success'] = True
    return api.build_capsule(response)
