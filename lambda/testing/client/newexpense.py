#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': "my_uuid",
            'title': 'another_expense',
            'total': 13,
            'expense': {'test@test.test': 13},
            'owner': 'm@email.com', 
            'request_time': 'now', 
            'due_date': 'later'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://osggc3wtegomn5yliv5heqkpji0ohbfk.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()