#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'email': 'lcover@purdue.edu'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://al53x3tpmf65idl4fujgprneya0ulsfd.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()