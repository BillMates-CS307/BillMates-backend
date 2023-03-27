import json
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.api as api

def lambda_handler(event, context):
    token = event['headers']['token']
    response = {}
    # check token
    response['token_success'] = api.check_token(token)
    
    if response['token_success']:
        db = mongo.get_database()
        parameters = json.loads(event['body'])
        
        email = parameters['email']
        user = mongo.query_table('users', {'email': email}, db)
        group_id = parameters['group_id']
        total = parameters['total']
        balance = mongo.user_balance_in_group(email, group_id, db) 
        expenses = parameters['expenses']
        
        if total > -balance or total <= 0:
            response['pay_success'] = False
            return api.build_capsule(response)
        response['pay_success'] = True
        
        message = user['name'] + ' has paid back '
        if balance == -total:
            message += 'their balance in full'
        else:
            message += '$' + str(total) + ' of their balance'
       
        users = []
        for e in expenses:
            users.append([e, expenses[e]])
        
        new_expense = {
            'title': message,
            'amount': total,
            'users': users,
            'owner': email,
            'group_id': group_id,
            'is_payout': True
        }
        
        group = mongo.query_table('groups', {'uuid': group_id}, db)
        
        oid = db['expenses'].insert_one(new_expense).inserted_id
        group['expenses'].append(oid)
        new_val = {'expenses': group['expenses']}
        db['groups'].update_one({'uuid': group_id}, {'$set': new_val})
    
    return api.build_capsule(response)
