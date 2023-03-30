import json
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.api as api
from bson.objectid import ObjectId


def lambda_handler(event, context):
    token = event['headers']['token']
    response = {}

    # token verification
    response['token_success'] = api.check_token(token)

    if response['token_success']:
        db = mongo.get_database()
        pending = db['pending_paid_expenses']
        
        # retrieving parameters
        parameters = json.loads(event['body'])
        
        group_id = parameters['group_id']
        email = parameters['email']
        group = mongo.query_table('groups', {'uuid': group_id}, db)
        
        if group is None:
            response['get_success'] = False
            return api.build_capsule(response)
        response['get_success'] = True
        
        g_requests = group['expenses']
        g_members = group['members']
        name = group['name']
        requests = []
        members = {}
        for r in g_requests:
            expense = mongo.query_table('expenses', {'_id': r}, db)
            expense['_id'] = str(expense['_id'])
            requests.append(expense)
        response['balances'] = {}
        for m in g_members:
            members[m] = mongo.query_table('users', {'email': m}, db)['name']
            response['balances'][m] = mongo.user_balance_in_group(m, group_id, db)
        response['members'] = members
        response['all_time_members'] = group['all_time_members']
        response['expenses'] = requests
        response['name'] = name
        response['manager'] = str(group['manager'])
        response['balance'] = mongo.user_balance_in_group(email, group_id, db)
        response['pending'] = list(pending.find({'paid_to': email}))
        response['settings'] = dict(group['settings'])
        
        temp_list = []
        for p in response['pending']:
            if p['group_id'] == group_id:
                p['expense_id'] = str(p['expense_id']) 
                p['_id'] = str(p['_id'])
                temp_list.append(p)
        response['pending'] = temp_list
    return api.build_capsule(response)