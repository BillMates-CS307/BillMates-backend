#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'email': "bruhmoment", "uuid":"ce8d4671-d2cc-4306-85a3-fcac6a939816"}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://cxt3kig2ocrigm3mvzm7ql3m6u0plfwd.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
