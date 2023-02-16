#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    resp = requests.get(url)
    return resp.json()

def main():
    my_json = grab_json_from_url("https://jwfjuifdunib5gmornhrs4nm4a0pitnm.lambda-url.us-east-2.on.aws/?token=zpdkwA.2_kLU@zg")
    print("Works")

main()