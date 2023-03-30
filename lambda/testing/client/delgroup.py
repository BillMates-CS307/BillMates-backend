#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id' : '49302c2a-cb11-4399-8998-d15f40031e1c'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://zp6hyrzgyuocojaqm6ahxc5wxm0rjujf.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
