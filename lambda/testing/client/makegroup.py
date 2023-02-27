#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'name':'cool-group', 'manager':'benlilly'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://wwr7yimislgmw7f5crxlnqmxxq0prart.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
