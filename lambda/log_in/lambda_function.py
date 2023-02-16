import json
import requests

def grab_json_from_url(url: str):
    resp = requests.get(url)
    return resp.json()

def lambda_handler(event, context):
    
    # Parameters
    payload = event['queryStringParameters']
    
    # Verify token is correct before running more commands
    token = event['headers']['token']
    response = {"echo" : payload, "response": {}}
    
    verification = grab_json_from_url("https://cdv3yr23omakr4fkrtqgbpeela0zejwf.lambda-url.us-east-2.on.aws/?token=" + token)
    response['response']["verified"] = verification['response']
    
    
    return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(response)
    }