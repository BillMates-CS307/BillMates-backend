import json

def check_token(token: str):
    with open('tokens.json') as f:
        obj = json.load(f)
        if token in obj['tokens']:
            return True
    return False

# Driver
def lambda_handler(event, context):
    
    # Grab payloads and format response
    payloads = event['queryStringParameters']
    response = {"echo" : payloads, "response" : check_token(payloads['token'])} #check_token(payloads['token'])
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
