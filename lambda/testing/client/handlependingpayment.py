#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'accepted': True, 'expense_id':'640120c78720de1416c8214f'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://jfynig6bitelqawn2z4pv7rg440wnwjw.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()