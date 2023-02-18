import json
import requests
import email
import bundle.api as api
    
def check_database(data: dict, action: int) -> bool:
    url = "https://2nc74mmtjrt36ld4maqz3ibryi0ztygw.lambda-url.us-east-2.on.aws/"
    return api.grab_json_from_url(url, {'action':action}, data)
    
def lambda_handler(event, context):
    
    # Parameters
    payload = json.loads(event['body'])
    # Verify token is correct before running more commands
    token = event['headers']['token']
    response = {"echo" : payload, "response": {}}
    
    verification = api.grab_json_from_url("https://cdv3yr23omakr4fkrtqgbpeela0zejwf.lambda-url.us-east-2.on.aws/?token=" + token)
    response['response']["token_verified"] = verification['response']
    
    # Fake database for testings
    if verification['response']:
        response['response']['success'] = check_database(payload, 'CHECK')['response']['success']
    
    return api.build_capsule(response)