import json
import requests
import email
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
    
def check_database(data: dict) -> bool:
    query = {'email':data['email'], 'password':data['password']}
    return mongo.query_user(query) != None
    
def lambda_handler(event, context):
    
    # Parameters
    payload = json.loads(event['body'])
    
    # Build reponse JSON
    response = {"echo" : payload, "response": {}}

    # Verify token is correct before running more commands
    token = event['headers']['token']
    response['response']["token_success"] = api.check_token(token)
    
    # Match against database
    if response['response']["token_success"]:
        response['response']['login_success'] = check_database(payload)
    
    return api.build_capsule(response)