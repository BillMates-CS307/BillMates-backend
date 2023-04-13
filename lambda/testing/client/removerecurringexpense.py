#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {
        'recurring_expense_id': 'a5ecbb41-023e-4059-8df3-bfe05513ed96',
        'group_id': '6accc963-4d89-45a6-a7d1-eede888aacb8'
    }
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://blrjgnkgkeggkgoiagtgktfgfy0xiemu.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
