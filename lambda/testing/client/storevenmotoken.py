#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'email':'rdrittner@gmail.com', 'venmo_token': 'balls'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://hq56rve3ccdasnkl45tedppqgu0cshgn.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()