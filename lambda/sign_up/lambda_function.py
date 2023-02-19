import os
import json
import requests

def access_mongodb():
    mongodb_uri = os.environ['MONGODB_URI']
    client = pymongo.MongoClient(mongodb_uri)
    db = client.billmates
    return db

def grab_json_from_url(url: str):
    resp = requests.get(url)
    return resp.json()

def lambda_handler(event, context):
    db = access_mongodb()
    
    token = event['headers']['token']
    response = {"echo" : "None", "response": {}}
    
    # token verification
    verification = grab_json_from_url("https://cdv3yr23omakr4fkrtqgbpeela0zejwf.lambda-url.us-east-2.on.aws/?token=" + token)
    response['response']["verified"] = verification['response']
    
    if verification['response']:
        # retrieving parameters
        parameters = json.loads(event['body'])
        username = parameters['email']
        password = parameters['password']
        
        # Query database to determine if username available
        # If available add username and password to database and return success
        # If not return failure
        
        with open("pho_db.json") as f:
            obj = json.load(f)
            if username in obj['ledger']:
                response['details'] = 'failure'
            else:
                response['details'] = 'success'
                # add username and passsword to database
        
        return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps(response)
        }