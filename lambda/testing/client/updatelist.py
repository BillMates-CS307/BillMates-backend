#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'list_id' : '642d9577259e83029d17a2ae', 'item_name': 'item_lol', 'remove_item': False}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://ce6mzuwdkc7ebhnuxbik42hz5q0xxekz.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
