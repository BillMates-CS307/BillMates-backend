#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': "cf47bc91-6a73-45c4-9d0e-83721b3c3fe7",
            'title': 'anotha one',
            'comment': '(. )( .)',
            'total': 10,
            "tag" : "No Tag",
            'expense': {'bb2': 10},
            'owner': 'bb1'
            }
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://osggc3wtegomn5yliv5heqkpji0ohbfk.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()