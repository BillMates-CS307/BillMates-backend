#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': "6accc963-4d89-45a6-a7d1-eede888aacb8",
            'title': 'anotha one',
            'comment': '(. )( .)',
            'total': 10,
            'expense': {'rrittner@purdue.edu': 10},
            'owner': 'rdrittner@gmail.com'
            }
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://osggc3wtegomn5yliv5heqkpji0ohbfk.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()