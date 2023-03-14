import sys
import traceback
# change to absolute path on local machine
sys.path.append('C:\\Users\\rdrit\\OneDrive\\Documents\\GitHub\\BillMates-backend\\lambda\\python\\bundle')
import mongo
from bson import ObjectId
from pymongo import MongoClient

def main():
    query_user_test()


def query_user_test():
    db = mongo.get_database() 
    # creating temporary items that will be stored in user's fields
    # that will also be inserted into database. These act as the control
    # to verify that valid items are not deleted
    temp_group = db['groups'].insert_one({'uuid': 'new_uuid'}).inserted_id
    temp_group_uuid = db['groups'].find_one({'_id': temp_group})['uuid']
    temp_notif = db['notifications'].insert_one({}).inserted_id
    temp_expense = db['expenses'].insert_one({}).inserted_id
    # the invalid ObjectId that will be inserted into the user's fields
    # that does not exist in db and should be deleted
    fake_object_id = ObjectId('6410cb90c76fb027023b0000')
    # the user being inserted
    input_user = {
        'name': 'Ryan Rittner',
        'email': 'rrittner@purdue.edu',
        'password': '1234',
        'groups': ['non-existent uuid', 'another fake uuid'],
        'settings': {
            'notification': 'only email'
        },
        'notifications': [fake_object_id, temp_notif],
        'attempts': 0,
        'expenses': [fake_object_id, temp_expense]
    }
    # save the _id so that the user can be deleted after the test
    test_user = db['users'].insert_one(input_user).inserted_id
    # everything from here on until the item deletion in a try catch so
    # that if an error occurs the items still get deleted
    try:
        # the returned user and the expected result
        actual = mongo.query_table('users', {'email': 'rrittner@purdue.edu'})
        expected = {
            '_id': test_user,
            'name': 'Ryan Rittner',
            'email': 'rrittner@purdue.edu',
            'password': '1234',
            'groups': [],
            'settings': {
                'notification': 'only email'
            },
            'notifications': [temp_notif],
            'attempts': 0,
            'expenses': [temp_expense]
        }
        # verifying correctness
        if not actual == expected:
            print('QUERY_USER FAILURE\nactual:')
            print(actual)
            print('expected')
            print(expected)
        else:
            print('query_user success')
    # if an error occurs print stack trace
    except Exception as e:
        print('uh oh you got an error')
        traceback.print_exc(e)
    # delete inserted test items
    db['groups'].delete_one({'_id': temp_group})
    db['notifications'].delete_one({'_id': temp_notif})
    db['expenses'].delete_one({'_id': temp_expense})
    db['users'].delete_one({'_id': test_user})

def query_group_test():
    obj = mongo.query_table('groups', {'uuid': 'something'})
    print(obj)

def query_expense_test():
    obj = mongo.query_table('expense', {'_id': 'something'})
    print(obj)

def query_notification_test():
    obj = mongo.query_table('groups', {'_id': 'something'})
    print(obj)

def query_pending_test():
    obj = mongo.query_table('pending_paid_expense', {'_id': 'something'})
    print(obj)

main()