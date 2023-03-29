#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {
        'email':'rrittner@purdue.edu',
        'notification': 'only billmates'
    }
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://yimbhwmzyzeikdbjqylkdonwoy0czhwq.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()