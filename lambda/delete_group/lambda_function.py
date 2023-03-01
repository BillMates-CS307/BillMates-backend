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
        # retrieving collections
        db = mongo.get_database()
        expenses = db['expenses']
        users = db['users']
        groups = db['groups']
        pending_expenses = db['pending_paid_expenses']

        # retrieving parameters
        parameters = json.loads(event['body'])
        if not api.check_body(['group_id'], parameters):
            response['ERROR'] = 'malformed body'
            return api.build_capsule(response)
        group_id = parameters['group_id']
        
        # group_exists
        if groups.find_one({'uuid': group_id}) is None:
            response['delete_success'] = False
            return api.build_capsule(response)
        response['delete_success'] = True
        
        # getting objects
        group = groups.find_one({'uuid': group_id})
        g_expenses = list(expenses.find({'group_id': group_id}))
        g_payments = list(pending_expenses.find({'group_id': group_id}))
        users_list = list(users.find())
        g_users = []
        for u in users_list:
            u_groups = u['groups']
            for g in u_groups:
                if g['group_id'] == group_id:
                    g_users.append(u['email'])
        
        # send notification to all users
        
        # delete group from groups:
        groups.delete_one({'uuid': group_id})
        
        # delete group from users:
        for e in g_users:
            u = users.find_one({'email': e})
            for g in u['groups']:
                if g['group_id'] == group_id:
                    del g
            new_val = {'groups': u['groups']}
            users.update_one({'email': e}, {'$set': new_val})
        
        # delete expenses
        for e in g_payments:
            expenses.delete_one({'_id': e['_id']})
        
        # delete payments
        for p in g_expenses:
            pending_expenses.delete_one({'_id': p['_id']})
        
        
    return api.build_capsule(response)

