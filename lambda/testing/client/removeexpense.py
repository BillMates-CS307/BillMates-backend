#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'expense_id': '643f5c98ecf0003c9de3abed', 'remove': True}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://2xtgpr37spnenjmrurwm26mel40apwki.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
