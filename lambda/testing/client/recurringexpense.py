#!/usr/bin/python3

import json
import requests

def grab_json_from_url(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {
        'start_time': '13:22:00',
        'start_date': '2023-04-11',
        'frequency': 'daily',
        'group_id': "6accc963-4d89-45a6-a7d1-eede888aacb8",
        'title': '1:22d',
        'comment': 'yay',
        'total': 10,
        'tag': 'No Tag',
        'expense': {'rrittner@purdue.edu': 10},
        'owner': 'rdrittner@gmail.com'
    }
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main():
    my_json = grab_json_from_url('https://c6z6xbilcykvustu5h3jpdy3ty0znsge.lambda-url.us-east-2.on.aws/')
    print(my_json)

main()
