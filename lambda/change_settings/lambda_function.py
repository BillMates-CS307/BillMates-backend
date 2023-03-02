import os
import json
import requests
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.api as api


def grab_json_from_url(url: str):
    resp = requests.get(url)
    return resp.json()


def lambda_handler(event, context):
    token = event['headers']['token']
    response = {}

    # token verification
    response['token_success'] = api.check_token(token)

    if response['token_success']:
        db = mongo.get_database()

        # retrieving parameters
        parameters = json.loads(event['body'])
        email = parameters['email']
        # retrieve collection and user
        users = db['users']
        user = users.find_one({'email': email})
        # check if new password and name are provided
        password = None
        name = None
        notification = None
        if 'newPassword' in parameters:
            if parameters['oldPassword'] == None or not parameters['oldPassword'] == user['password']:
                response['change_success'] = False
                return api.build_capsule(response)
            password = parameters['newPassword']
        if 'name' in parameters:
            name = parameters['name']
        if 'notification' in parameters:
            notification = parameters['notification']
        
        if user is None:
            # if no user has email, user doesn't exist and return failure
            response['change_success'] = False
        else:
            # update necessary fields
            query = {'email': email}
            # new_val = {}
            # settings = users.find(query, 'settings')
            # if 'notification' not in settings:
            #     new_val['notifications' = 'both']
            #     users.update_one(query, {'$set': new_val})
            new_val = {}
            if not password == None:
                new_val['password'] = password
            if not name == None:
                new_val['name'] = name
            if not notification == None:
                new_val['settings'] = {}
                new_val['settings']['notification'] = notification
            users.update_one(query, {'$set': new_val})
            response['change_success'] = True

    return api.build_capsule(response)
