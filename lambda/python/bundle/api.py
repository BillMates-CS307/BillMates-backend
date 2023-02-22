import json
import requests

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