#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id' : 'uuid', 'name' : 'new_list'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://6dx5inbxxngfwkbmcwzl44tyla0vaoeh.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
