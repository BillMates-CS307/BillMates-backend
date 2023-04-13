#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {
        'group_id': '6accc963-4d89-45a6-a7d1-eede888aacb8',
        'event_id': '901cd865-21d6-42f0-96bf-5f10e0ad9793'
    }
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://dgsibjvgdor7elkqw3dbrybthy0izjkw.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()