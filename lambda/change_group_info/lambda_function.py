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
        uuid = parameters['group_id']
        # retrieve collection and user
        group = mongo.query_table('groups', {'uuid': uuid}, db)
        groups = db['groups']
        # check if new password and name are provided
        fufillment =  group['settings']['fufillment']
        auto_approve =  group['settings']['auto_approve']
        max_char =  group['settings']['max_char']
        if 'fufillment' in parameters:
            fufillment = parameters['fufillment']
        if 'auto_approve' in parameters:
            auto_approve = parameters['auto_approve']
        if 'max_char' in parameters:
            max_char = parameters['max_char']
        if group == None:
            # if no user has email, user doesn't exist and return failure
            response['change_success'] = False
        else:
            # update necessary fields
            query = {'uuid': uuid}
            new_val = {}
            new_val['fufillment'] = fufillment
            new_val['auto_approve'] = auto_approve
            new_val['max_char'] = max_char
            groups.update_one(query, {'$set': {'settings': new_val}})
            response['change_success'] = True

    return api.build_capsule(response)
