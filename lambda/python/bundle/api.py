import json
import requests

variables = {
    "tokens" : 
    set([
        "zpdkwA.2_kLU@zg"
    ])
}

def build_capsule(response: dict) -> dict:
    return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(response)
    }

def grab_json_from_url(url: str, headers=None, data=None) -> dict:
    resp = requests.post(url, json=data, headers=headers)
    return resp.json()

def check_token(token: str) -> bool:
    if token in variables['tokens']:
        return True
    return False

# Given the list of fields and the payload, returns 
# true if payload fields match given fields.
def check_body(fields: list, payload: dict) -> bool:
    if set(fields) == set(payload.keys()):
        return True
    return False
