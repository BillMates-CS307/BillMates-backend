#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'expense_id': "63fd495d86cc16ec750c1940",
            'email': 'test@test.test',
            'amount': 13}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://q6dj43wfjfvztvxbhdyqogvn2y0gfcro.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()