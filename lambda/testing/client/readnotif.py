#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'object_id' : '641282ab6f77843e54dae978'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://wzqss3razlwkrdnwdm6nr4vx6i0rxnqn.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
