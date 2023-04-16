#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'email':'ben@ben.ben', 'password':'ben', 'name': 'ben'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://rdsn74oehsmrcoc2spf6aiw4iy0hqcbv.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()