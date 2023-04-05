#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id' : '0a521fc0-c9cd-405d-bdc6-d471e936922f'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://insa5ebljuef64fgncauekqrgq0lerzj.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
