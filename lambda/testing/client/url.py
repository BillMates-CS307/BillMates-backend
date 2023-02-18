#!/usr/bin/python3

import json
import requests
from enum import Enum

class Action(Enum):
    TEST=1
    BRO=2

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'email':'bhlilley@purdue.edu', 'password':'my_pass'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def bro(action: Action):
    return action 

def main():
    my_json = grab_json_from_url('https://jwfjuifdunib5gmornhrs4nm4a0pitnm.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
