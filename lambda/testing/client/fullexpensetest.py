#!/usr/bin/python3

import json
import requests

uuid = "3c2fbeb8-15c4-4b17-95f8-7019c17493bc"

def setup():
    # sign up both users
    surl = 'https://rdsn74oehsmrcoc2spf6aiw4iy0hqcbv.lambda-url.us-east-2.on.aws/'
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'email':'rdrittner@gmail.com', 'password':'pass', 'name': 'Ryan Gmail'}
    requests.post(surl, headers=headers, json=body)
    body = {'email':'rrittner@purdue.edu', 'password':'pass', 'name': 'Ryan Purdue'}
    requests.post(surl, headers=headers, json=body)
    # make group
    murl = 'https://wwr7yimislgmw7f5crxlnqmxxq0prart.lambda-url.us-east-2.on.aws/'
    body = {'name':'full_expense_test_group', 'manager':'rdrittner@gmail.com'}
    requests.post(murl, headers=headers, json=body)
    # get uuid
    uurl = 'https://spdzmxp6xdfjiwptqdabqgcy4q0rmcwt.lambda-url.us-east-2.on.aws/'
    body = {'email': 'rdrittner@gmail.com'}
    resp = requests.post(uurl, headers=headers, json=body)

    uuid = resp.json()['user']['groups'][0]
    # add other user to group
    aurl = 'https://cxt3kig2ocrigm3mvzm7ql3m6u0plfwd.lambda-url.us-east-2.on.aws/'
    body = {'email': "rrittner@purdue.edu", "uuid":uuid}
    print(requests.post(aurl, headers=headers, json=body).json())

def get_group_info_json():
    url = 'https://jujezuf56ybwzdn7edily3gu6a0dcdir.lambda-url.us-east-2.on.aws/'
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': uuid, 'email': 'rrittner@purdue.edu'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()
    

def new_expense_json(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': uuid,
            'title': 'new_expense!!',
            'total': 10,
            'expense': {'rdrittner@gmail.com': 10},
            'owner': 'rrittner@purdue.edu'
            }
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def pay_expense_json(url: str, expense_id) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'expense_id': expense_id,
            'email': 'rdrittner@gmail.com',
            'amount': 10}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def payment_fulfilled_json(url: str, accepted, payment_id) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'accepted': accepted, 'payment_id': payment_id}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def main(): # not done
    nurl = 'https://osggc3wtegomn5yliv5heqkpji0ohbfk.lambda-url.us-east-2.on.aws/'
    purl = 'https://q6dj43wfjfvztvxbhdyqogvn2y0gfcro.lambda-url.us-east-2.on.aws/'
    furl = 'https://jfynig6bitelqawn2z4pv7rg440wnwjw.lambda-url.us-east-2.on.aws/'

    new_expense = new_expense_json(nurl)
    if new_expense['submit_success'] != True:
        print("new_expense (1) error")
        print(new_expense)
        return
    print('new_expense (1) success')

    expense_id = get_group_info_json()['expenses'][0]['_id']
    new_payment = pay_expense_json(purl, expense_id)
    if new_payment['pay_success'] != True:
        print('pay_expense (1) error')
        print(new_payment)
        return
    print('new_payment (1) success')

    payment_id = get_group_info_json()['pending'][0]['_id']
    new_fulfill = payment_fulfilled_json(furl, False, payment_id)
    if new_fulfill['handle_success'] != True:
        print('fulfill_payment (1) error')
        print(new_fulfill)
        return
    print('new_fulfill (1) success')

    new_payment2 = pay_expense_json(purl, expense_id)
    if new_payment2['pay_success'] != True:
        print('pay_expense (2) error')
        print(new_payment2)
        return
    print('new_payment (2) success')

    payment_id2 = get_group_info_json()['pending'][0]['_id']
    new_fulfill2 = payment_fulfilled_json(furl, True, payment_id2)
    if new_fulfill2['handle_success'] != True:
        print('fulfill_payment (2) error')
        print(new_fulfill2)
        return
    print('new_fulfill (2) success')

main()