import json
import requests
import email

def grab_json_from_url(url: str):
    resp = requests.get(url)
    return resp.json()

def lambda_handler(event, context):
    
    # Parameters
    payload = json.loads(event['body'])
    # Verify token is correct before running more commands
    token = event['headers']['token']
    response = {"echo" : payload, "response": {}}
    
    verification = grab_json_from_url("https://cdv3yr23omakr4fkrtqgbpeela0zejwf.lambda-url.us-east-2.on.aws/?token=" + token)
    response['response']["token_verified"] = verification['response']
    
    # Fake database for testings
    if verification['response']:
        usr, pw = payload['email'], payload['password']
        with open("pho_db.json") as f:
            obj = json.load(f)
            response['response']['success'] = usr in obj['ledger'] and obj['ledger'][usr] == pw
    return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(response)
    }