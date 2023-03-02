#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': "4505d575-373d-43a5-afd8-e0d5dcade172",
            'title': 'g_pays_p_10',
            'total': 10,
            'expense': {'rdrittner@gmail.com': 10},
            'owner': 'rrittner@purdue.edu'
            }
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://osggc3wtegomn5yliv5heqkpji0ohbfk.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()