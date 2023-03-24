#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id' : '67c1548d-8f7b-47e0-8819-1442a8237186'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://zy2ttsd3w5vhxsdv5ty6t7e6h40gdcbr.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
