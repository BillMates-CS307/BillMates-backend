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
    response = {"echo": "None", "response": {}}

    # token verification
    response['response']["verified"] = api.check_token(token)

    if response['response']["verified"]:
        db = mongo.get_database()

        # retrieving parameters
        parameters = json.loads(event['body'])
        email = parameters['email']
        password = parameters['password']
        name = parameters['name']

        users = db['users']
        user = mongo.query_user({'email': email})
        if user is None:
            new_user = {
                'email': email,
                'password': password,
                'name': name
            }
            users.insert_one(new_user)
            response['sign_up_success'] = True
        else:
            response['sign_up_success'] = False

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(response)
        }
