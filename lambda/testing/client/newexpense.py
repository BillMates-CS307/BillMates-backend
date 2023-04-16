#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': "f8ffb8a5-d1c8-4a87-9a54-27288c49a6a9",
            'title': 'anotha one',
            'comment': '(. )( .)',
            'total': 10,
            "tag" : "No Tag",
            'expense': {'ben2@ben.ben': 10},
            'owner': 'ben@ben.ben'
            }
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://osggc3wtegomn5yliv5heqkpji0ohbfk.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()