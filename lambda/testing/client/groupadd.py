#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'email': "test@test.test", "uuid":"7738066e-da1a-47a4-81b6-31904e768838"}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://cxt3kig2ocrigm3mvzm7ql3m6u0plfwd.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
