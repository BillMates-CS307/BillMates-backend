#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {
        'recurring_expense_id': 'a330f7ee-85e0-465c-a43f-00f51c11727d',
        'group_id': '6accc963-4d89-45a6-a7d1-eede888aacb8'
    }
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://blrjgnkgkeggkgoiagtgktfgfy0xiemu.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
