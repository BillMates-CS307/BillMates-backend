import json
import requests

def grab_json_from_url(url: str):
    resp = requests.get(url)
    return resp.json()

def lambda_handler(event, context):
    
    token = event['headers']['token']
    response = {"echo" : "None", "response": {}}
    
    # token verification
    verification = grab_json_from_url("https://cdv3yr23omakr4fkrtqgbpeela0zejwf.lambda-url.us-east-2.on.aws/?token=" + token)
    response['response']["verified"] = verification['response']
    
    # retrieving parameters
    parameters = event['queryStringParameters']
    username = parameters['username']
    password = parameters['password']
    
    # Query database to determine if username available
    # If available add username and password to database and return success
    # If not return failure
    
    # Query
    does_the_username_exist = False
    
    if not does_username_exist:
        response['response']['success'] = 'true'
    else:
        response['response']['success'] = 'false'
    
    return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(response)
    }
