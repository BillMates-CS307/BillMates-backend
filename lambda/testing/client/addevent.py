#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {
        'group_id' : '6accc963-4d89-45a6-a7d1-eede888aacb8',
        'email': 'rdrittner@gmail.com',
        'name': 'another event!!!',
        'description': 'no',
        'location': 'somewhere',
        'date': '2023-04-11',
        'time': '10:10:10'
    }
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://nujjvkoiihad67dlfsarvzotsa0zpnbz.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
