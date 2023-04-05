#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id' : 'uuid'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://evu7t6kskxh6wk7tj3cwfw7dyq0tsczh.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
