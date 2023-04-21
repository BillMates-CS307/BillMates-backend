#!/usr/bin/python3

import json
import requests
import random
import string

rand_str = ''.join(random.choices(string.ascii_letters, k=7))
total = 0

def grab_json_from_url(url: str, body: dict) -> json:
    headers = {'token': 'zpdkwA.2_kLU@zg'}
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

def make_group():
    body = {'name': rand_str, 'manager':rand_str}
    grab_json_from_url("https://wwr7yimislgmw7f5crxlnqmxxq0prart.lambda-url.us-east-2.on.aws/", body)
    group_id = grab_json_from_url("https://spdzmxp6xdfjiwptqdabqgcy4q0rmcwt.lambda-url.us-east-2.on.aws/", {'email':rand_str})['user']['groups'][~0]['uuid']
    grab_json_from_url("https://cxt3kig2ocrigm3mvzm7ql3m6u0plfwd.lambda-url.us-east-2.on.aws/", {'email': f"{rand_str}-2", "uuid":group_id})
    return group_id

def printC(string, boolean):
    global total
    if boolean:
        total += 1
        print("\033[92m" + string + "\033[0m")
    else:
        print("\033[91m" + string + "\033[0m")

def plus():
    print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

######
grab_json_from_url('https://rdsn74oehsmrcoc2spf6aiw4iy0hqcbv.lambda-url.us-east-2.on.aws/', {'email':rand_str, 'password':'sprint3', 'name': 'sprint3'})
grab_json_from_url('https://rdsn74oehsmrcoc2spf6aiw4iy0hqcbv.lambda-url.us-east-2.on.aws/', {'email':rand_str + '-2', 'password':'sprint3-2', 'name': 'sprint3-2'})
person_one = rand_str
person_two = rand_str + '-2'
group_id = make_group()
######

print(f"Sprint 3 --- Backend All-Encompassing Test Module --- \n======================================================")

print("\nUser Story #1 - Shopping List Creation")

response = grab_json_from_url("https://6dx5inbxxngfwkbmcwzl44tyla0vaoeh.lambda-url.us-east-2.on.aws/", \
                              {'group_id' : group_id, 'name' : rand_str })

printC(f"\nUser Story #1 - Passed: {response['create_success']}", response['create_success'])

plus()

###############

response = grab_json_from_url("https://evu7t6kskxh6wk7tj3cwfw7dyq0tsczh.lambda-url.us-east-2.on.aws/", \
                              {'group_id' : group_id})

shop_list = response['shopping_lists'][~0]

##############


print("\nUser Story #2 - Shopping List Updates (Remove/Add Item)")

response = grab_json_from_url("https://ce6mzuwdkc7ebhnuxbik42hz5q0xxekz.lambda-url.us-east-2.on.aws/", \
                              {'list_id' : shop_list['_id'], 'item_name': rand_str, 'remove_item': False})

response = grab_json_from_url("https://ce6mzuwdkc7ebhnuxbik42hz5q0xxekz.lambda-url.us-east-2.on.aws/", \
                              {'list_id' : shop_list['_id'], 'item_name': rand_str, 'remove_item': True})

printC(f"\nUser Story #2 - Passed: {response['change_success']}", response['change_success'])

plus()
#################################

print("\nUser Story #4/6 - Grab Calendar Info (Group and User)")

response = grab_json_from_url("https://insa5ebljuef64fgncauekqrgq0lerzj.lambda-url.us-east-2.on.aws/", \
                              {'group_id' : group_id})

correct = response['get_success']

response = grab_json_from_url('https://6b7hetv76hhwtm6ewy2ucl5sry0knann.lambda-url.us-east-2.on.aws/', \
                              {'email' : person_one})

correct = correct and response['get_success']

printC(f"\nUser Story #4/6 - Passed: {correct}", correct)

plus()
#################################

print("\nUser Story #5 - Add and Remove Events")

body = {
        'group_id' : group_id,
        'email': person_one,
        'name': rand_str,
        'description': 'no',
        'location': 'somewhere',
        'date': '2023-04-28',
        'time': '10:10:10'
    }

response = grab_json_from_url("https://nujjvkoiihad67dlfsarvzotsa0zpnbz.lambda-url.us-east-2.on.aws/", \
                              body)
correct = response['add_success']

response = grab_json_from_url("https://insa5ebljuef64fgncauekqrgq0lerzj.lambda-url.us-east-2.on.aws/", \
                              {'group_id' : group_id})
event_id = response['events'][~0]['id']

response = grab_json_from_url("https://dgsibjvgdor7elkqw3dbrybthy0izjkw.lambda-url.us-east-2.on.aws/", \
                              {'group_id' : group_id, 'event_id' : event_id})

correct = response['remove_success'] and correct

printC(f"\nUser Story #5 - Passed: {correct}", correct)

plus()

########################


print("\nUser Story #7 - Add and Remove Recurring Expenses")

body = {
        'start_time': '13:22:00',
        'start_date': '2023-04-20',
        'frequency': 'daily',
        'group_id': group_id,
        'title': rand_str,
        'comment': 'yay',
        'total': 10,
        'tag': 'No Tag',
        'expense': {person_two: 10},
        'owner': person_one
    }

response = grab_json_from_url("https://c6z6xbilcykvustu5h3jpdy3ty0znsge.lambda-url.us-east-2.on.aws/", \
                              body)
correct = response['submit_success']

printC(f"\nUser Story #7 - Passed: {correct}", correct)

plus()

#######################

print("\nUser Story #8 - View Analytics (Group and User)")

response = grab_json_from_url("https://hui6d6bjvtgpaydsi5c6ykoy2y0amwxs.lambda-url.us-east-2.on.aws/", \
                              {'email' : person_one})

correct = response['get_success']

printC(f"\nUser Story #8 - Passed: {correct}", correct)

plus()

#######################

print("\nUser Story #9 - Tag Transactions")

body = {'group_id': group_id,
            'title': rand_str,
            'comment': rand_str,
            'total': 10,
            "tag" : "Entertainment",
            'expense': {person_two: 10},
            'owner': person_one
        }

response = grab_json_from_url("https://osggc3wtegomn5yliv5heqkpji0ohbfk.lambda-url.us-east-2.on.aws/", \
                              body)

correct = response['submit_success']

printC(f"\nUser Story #9 - Passed: {correct}", correct)

plus()
print("\033[92mSprint 3 Backend All-Encompassing Test Module Complete\033[0m")
print(f"Total Score: {total}/7")
plus()

#########################
