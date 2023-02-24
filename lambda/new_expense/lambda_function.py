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
        # retrieving parameters
        parameters = json.loads(event['body'])
        title = parameters['title']  # title of expense
        group = parameters['group_id']  # group_id for expense
        u_expenses = parameters['expense']  # dict of form { 'email_of_user' : amount_owed }
        request_time = parameters['request_time']  # time created
        due_date = parameters['due_date']  # when expense is due
        # notification when due date is reached?
        total = 0
        # make sure that total of owed money for each user = total for first user
        check_total = 0
        failure = False
        for u_email in u_expenses:
            # first loop to check that all users are in group and that expense totals add up
            user_groups = users.find({'email': u_email}, 'groups')
            if not group in user_groups:  # if user not in expense's group, return failure
                failure = True
            if expenses[u_email] < 0:
                failure = True
            if total == 0:  # user who submitted expense
                total += expenses[u_email]
            else:  # users who owe money
                check_total += expenses[u_email]
        if not check_total == total:
            # if totals are not equal
            failure = True
        if failure:
            response['submit_success'] = False
            return api.build_capsule(response)
        total = 0
        for u_email in u_expenses:
            # loop to update group balance of each user
            user_groups = users.find({'email': u_email}, 'groups')
            if total == 0:  # user who submitted expense
                user_groups[group] += expenses[u_email]
                total += expenses[u_email]
            else:  # users who owe money
                user_groups[group] -= expenses[u_email]
            new_val = {'groups': user_groups}
            users.update_one({'email': u_email}, {'$set': new_val})
            # send notification?

        # add expense to database
        new_expense = {
            'group_id': group,
            'title': title,
            'users': u_expenses,
            'amount': total,
            'due_date': due_date,
            'request_time': request_time
        }
        users.insert_one(new_expense)
        response['submit_success'] = True
    return api.build_capsule(response)
