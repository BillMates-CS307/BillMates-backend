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
        groups = db['groups']
        users = db['users']
        expenses = db['expenses']
        pending = db['pending_paid_expenses']
        
        # retrieving parameters
        parameters = json.loads(event['body'])
        
        group_id = parameters['group_id']
        email = parameters['email']
        group = groups.find_one({'uuid': group_id})
        
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
            expense = expenses.find_one({'_id': r})
            expense['_id'] = str(expense['_id'])
            requests.append(expense)
        for m in g_members:
            members[m] = users.find_one({'email': m})['name']
        response['members'] = members
        response['expenses'] = requests
        response['name'] = name
        response['manager'] = str(group['manager'])
        user_groups = users.find_one({'email': email})['groups']
        for g in user_groups:
            if g['group_id'] == group_id:
                response['balance'] = g['balance']
                
        response['pending'] = list(pending.find({'paid_to': email})) # returns a cursor
        temp_list = []
        for p in response['pending']:
            if p['group_id'] == group_id:
                p['expense_id'] = str(p['expense_id']) 
                p['_id'] = str(p['_id'])
                temp_list.append(p)
        response['pending'] = temp_list
    return api.build_capsule(response)