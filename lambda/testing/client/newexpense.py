#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': "my_uuid", 'title': 'my_expense5', 'total': 100, 'expense': {'m@email.com': 100},
            'owner': 'test@test.test', 'request_time': 'now', 'due_date': 'later'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://osggc3wtegomn5yliv5heqkpji0ohbfk.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()