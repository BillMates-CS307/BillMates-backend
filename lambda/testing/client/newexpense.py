#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': 0, 'title': 'my_expense', 'expense': {
        'email@email.com': 10,
        'other@email.com': 5,
        'e@mail.com': 5}, 'expense_time': '2000-01-01T05:00:00.000+00:00', 'due_date': '2000-01-01T05:00:00.000+00:00'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://osggc3wtegomn5yliv5heqkpji0ohbfk.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()