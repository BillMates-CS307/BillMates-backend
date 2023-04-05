#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'list_id' : '642d9577259e83029d17a2ae', 'isActive' : False}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://gdmqnuwrzqsja2ps3zc2z2y4km0ejbyu.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
