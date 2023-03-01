#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'object_id' : '63fe9533f687c0bde3b17788'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://jqzztp2tci2reghy5gkp5wlrsm0oqspd.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
