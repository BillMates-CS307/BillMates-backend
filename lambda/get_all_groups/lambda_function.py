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
        response = {}
        response['groups'] = []
        
        email = parameters['email']
        groups = mongo.query_table('users', {'email': email}, db)['groups']
        
        if groups is None:
            response['get_success'] = False
            return api.build_capsule(response)
        
        for g in groups:
            group = mongo.query_table('groups', {'uuid': g}, db)
            out = {}
        
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
            out['balances'] = {}
            for m in g_members:
                members[m] = mongo.query_table('users', {'email': m}, db)['name']
                out['balances'][m] = mongo.user_balance_in_group(m, g, db)
            out['members'] = members
            out['all_time_members'] = group['all_time_members']
            out['expenses'] = requests
            out['name'] = name
            out['settings'] = dict(group['settings'])
            out['manager'] = str(group['manager'])
            out['balance'] = mongo.user_balance_in_group(email, g, db)
            out['pending'] = list(pending.find({'paid_to': email}))
            out['group_id'] = str(g)
            out['archived'] = group['archived']
        
            temp_list = []
            for p in out['pending']:
                if p['group_id'] == g:
                    p['expense_id'] = str(p['expense_id']) 
                    p['_id'] = str(p['_id'])
                    temp_list.append(p)
            out['pending'] = temp_list
            
            response['groups'].append(out)
    return api.build_capsule(response)