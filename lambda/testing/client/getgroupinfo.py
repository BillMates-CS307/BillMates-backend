#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': '32d4ddbb-e56f-49c9-9f99-8eecafa00ce0', 'email': 'rdrittner@gmail.com'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://jujezuf56ybwzdn7edily3gu6a0dcdir.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()