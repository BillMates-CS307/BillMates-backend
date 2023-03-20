#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id' : 'f455993a-d8b1-4b4a-9ff7-8b0ad52b3aeb'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://zp6hyrzgyuocojaqm6ahxc5wxm0rjujf.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
