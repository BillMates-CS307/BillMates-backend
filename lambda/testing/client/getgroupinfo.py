#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': 'b52d8ec8-8d62-404d-a81e-8efe35ad7615', 'email': 'gsegura@purdue.edu'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://jujezuf56ybwzdn7edily3gu6a0dcdir.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()