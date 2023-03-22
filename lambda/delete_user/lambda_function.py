import json
from pymongo import MongoClient
import bundle.mongo as mongo
import bundle.api as api
from bson.objectid import ObjectId

def lambda_handler(event, context):
    
    payload = json.loads(event['body'])
    token = event['headers']['token']
    response = {}

    # token verification
    response['token_success'] = api.check_token(token)
    if response['token_success']:
        db = mongo.get_database()
        user = mongo.query_user({'email' : payload['email']}, False)
        for notif in user['notifications']:
            db['notifications'].delete_one({'_id' : ObjectId(notif)})
        db['users'].delete_one({'email' : payload['email']})
        response['delete_success'] = True

    return api.build_capsule(response)
