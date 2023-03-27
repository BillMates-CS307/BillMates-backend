#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': "3c2fbeb8-15c4-4b17-95f8-7019c17493bc",
            'title': 'anotha one',
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