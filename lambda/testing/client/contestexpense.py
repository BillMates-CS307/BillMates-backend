#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'expense_id': '64221b99d1c54c547aa62a57', 'email': 'rrittner@purdue.edu'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://ctxt572a2yvnjttpbcnloz6gem0fhzmo.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
