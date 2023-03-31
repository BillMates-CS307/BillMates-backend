#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {
        'email':'lee2058@purdue.edu',
        'name' : 'new name',
        'newPassword' : 'newpass',
        'oldPassword' : 'QWErty123!'
    }
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://b3s3uiqq5h7gbd7ay3kjhjl2ti0qnrmn.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()