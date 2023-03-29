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

def get_group_info_json(email):
    url = 'https://jujezuf56ybwzdn7edily3gu6a0dcdir.lambda-url.us-east-2.on.aws/'
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': uuid, 'email': email}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()
    

def new_expense_json(url: str) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    body = {'group_id': uuid,
            'title': 'new_expense!!',
            'comment': 'a comment',
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

def main(): # Make sure group has no expenses or payments when run
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    nurl = 'https://osggc3wtegomn5yliv5heqkpji0ohbfk.lambda-url.us-east-2.on.aws/'
    purl = 'https://q6dj43wfjfvztvxbhdyqogvn2y0gfcro.lambda-url.us-east-2.on.aws/'
    furl = 'https://jfynig6bitelqawn2z4pv7rg440wnwjw.lambda-url.us-east-2.on.aws/'
    burl = 'https://ipzfxhr6iinf5lohek6kvva3lu0wirji.lambda-url.us-east-2.on.aws/'
    curl = 'https://ctxt572a2yvnjttpbcnloz6gem0fhzmo.lambda-url.us-east-2.on.aws/'
    rurl = 'https://2xtgpr37spnenjmrurwm26mel40apwki.lambda-url.us-east-2.on.aws/'

    new_expense = new_expense_json(nurl)
    if new_expense['submit_success'] != True:
        print("new_expense (1) error")
        print(new_expense)
        return
    print('new_expense (1) success')

    expense_id = get_group_info_json('rrittner@purdue.edu')['expenses'][0]['_id']
    new_payment = pay_expense_json(purl, expense_id)
    if new_payment['pay_success'] != True:
        print('pay_expense (1) error')
        print(new_payment)
        return
    print('new_payment (1) success')

    payment_id = get_group_info_json('rrittner@purdue.edu')['pending'][0]['_id']
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

    payment_id2 = get_group_info_json('rrittner@purdue.edu')['pending'][0]['_id']
    new_fulfill2 = payment_fulfilled_json(furl, True, payment_id2)
    if new_fulfill2['handle_success'] != True:
        print('fulfill_payment (2) error')
        print(new_fulfill2)
        return
    print('new_fulfill (2) success')

    new_expense = new_expense_json(nurl)
    if new_expense['submit_success'] != True:
        print("new_expense (3) error")
        print(new_expense)
        return
    print('new_expense (3) success')  

    body = {
        'email': 'rdrittner@gmail.com', 
        'group_id': '3c2fbeb8-15c4-4b17-95f8-7019c17493bc',
        'total': 10,
        'expenses': {'rrittner@purdue.edu': 10}
    }
    resp = requests.post(burl, headers=headers, json=body)
    balance_payment = resp.json()
    if balance_payment['pay_success'] != True:
        print('balance_payment (1) error')
        print(balance_payment)
        return
    print('balance_payment (1) success')

    expense_id = get_group_info_json('rdrittner@gmail.com')['expenses'][0]['_id']
    body = {'expense_id': expense_id, 'email': 'rdrittner@gmail.com'}
    resp = requests.post(curl, headers=headers, json=body)
    contest_return = resp.json()
    if contest_return['contest_success'] != True:
        print('contest_expense (1) error')
        print(contest_return)
        return
    print('contest_expense (1) success')

    body = {'expense_id': expense_id, 'remove': False}
    resp = requests.post(rurl, headers=headers, json=body)
    remove_return = resp.json()
    if remove_return['remove_success'] != True:
        print('remove_expense (1) error')
        print(contest_return)
        return
    print('remove_expense (1) success')

    body = {'expense_id': expense_id, 'email': 'rdrittner@gmail.com'}
    resp = requests.post(curl, headers=headers, json=body)
    contest_return = resp.json()
    if contest_return['contest_success'] != True:
        print('contest_expense (2) error')
        print(contest_return)
        return
    print('contest_expense (2) success')

    body = {'expense_id': expense_id, 'remove': True}
    resp = requests.post(rurl, headers=headers, json=body)
    remove_return = resp.json()
    if remove_return['remove_success'] != True:
        print('remove_expense (2) error')
        print(contest_return)
        return
    print('remove_expense (2) success')

    balances = get_group_info_json('rdrittner@gmail.com')['balances']
    body = {
        'email': 'rrittner@purdue.edu', 
        'group_id': '3c2fbeb8-15c4-4b17-95f8-7019c17493bc',
        'total': 10,
        'expenses': {'rdrittner@gmail.com': 10}
    }
    resp = requests.post(burl, headers=headers, json=body)
    balance_payment = resp.json()
    if balance_payment['pay_success'] != True:
        print('balance_payment (2) error')
        print(balance_payment)
        return
    print('balance_payment (2) success')

    balances = get_group_info_json('rdrittner@gmail.com')['balances']
    if balances['rdrittner@gmail.com'] != 0 or balances['rrittner@purdue.edu'] != 0:
        print('balances incorrect')
        print(balance_payment)
        return
    print('balances correct')

    expenses = get_group_info_json('rdrittner@gmail.com')['expenses']
    expense_id1 = expenses[0]['_id']
    expense_id2 = expenses[1]['_id']

    body = {'expense_id': expense_id1, 'remove': True}
    resp = requests.post(rurl, headers=headers, json=body)
    remove_return = resp.json()
    if remove_return['remove_success'] != True:
        print('remove_expense (3) error')
        print(contest_return)
        return
    print('remove_expense (3) success')

    body = {'expense_id': expense_id2, 'remove': True}
    resp = requests.post(rurl, headers=headers, json=body)
    remove_return = resp.json()
    if remove_return['remove_success'] != True:
        print('remove_expense (4) error')
        print(contest_return)
        return
    print('remove_expense (4) success')

    print('Full test success')





main()