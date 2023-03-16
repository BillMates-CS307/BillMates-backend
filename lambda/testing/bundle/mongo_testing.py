import sys
import traceback
# change to absolute path on local machine
sys.path.append('C:\\Users\\rdrit\\OneDrive\\Documents\\GitHub\\BillMates-backend\\lambda\\python\\bundle')
import mongo
from bson import ObjectId
from pymongo import MongoClient

def main():
    query_expense_test()

def balance_test():
    db = mongo.get_database() 
    # creating temporary items
    temp_group_id = db['groups'].insert_one({'uuid': 'new_uuid'}).inserted_id
    temp_group_uuid = db['groups'].find_one({'_id': temp_group_id})['uuid']
    temp_user1 = db['users'].insert_one({'email': '1'}).inserted_id
    temp_user2 = db['users'].insert_one({'email': '2'}).inserted_id
    temp_user3 = db['users'].insert_one({'email': '3'}).inserted_id
    # expense
    input_expense = {
        'title': 'test_expense',
        'amount': 3,
        'owner': '1',
        'group_id': temp_group_uuid,
        'users': [('2', 3)]
    }
    test_expense = db['expenses'].insert_one(input_expense).inserted_id
    try:
        user_1_balance = mongo.user_balance_in_group('1', temp_group_uuid)
        user_2_balance = mongo.user_balance_in_group('2', temp_group_uuid)
        user_3_balance = mongo.user_balance_in_group('3', temp_group_uuid)
        if not (user_1_balance == 3 and user_2_balance == -3):
            print('USER_GROUP_BALANCE FAILURE\nactual:')
            print('user_1: ' + str(user_1_balance) + ', user_2: ' + str(user_2_balance) + ', user_3: ' + str(user_3_balance))
            print('actual:\nuser_1: 10, user_2: -3, user_3: 7')
        else:
            print('user_group_balance success')
    except Exception as e:
        print('uh oh you got an error')
        try:
            traceback.print_exc(e)
        except:
            print('?')
    db['users'].delete_one({'email': '1'})
    db['users'].delete_one({'email': '2'})
    db['users'].delete_one({'email': '3'})
    db['groups'].delete_one({'uuid': temp_group_uuid})
    db['expenses'].delete_one({'_id': test_expense})


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
        try:
            traceback.print_exc(e)
        except:
            print('?')
    # delete inserted test items
    db['groups'].delete_one({'_id': temp_group})
    db['notifications'].delete_one({'_id': temp_notif})
    db['expenses'].delete_one({'_id': temp_expense})
    db['users'].delete_one({'_id': test_user})

def query_group_test():
    obj = mongo.query_table('groups', {'uuid': 'something'})
    print(obj)

def query_expense_test():
    db = mongo.get_database() 
    # creating temporary items
    temp_group_uuid = 'new_uuid'
    temp_group = db['groups'].insert_one({'uuid': temp_group_uuid}).inserted_id
    # the user being inserted
    input_expense_valid = {
        'title': 'test_expense',
        'owner': 'someone',
        'amount': 5,
        'users': [['someone else', 5]],
        'group_id': temp_group_uuid
    }
    input_expense_invalid = {
        'title': 'test_expense2',
        'owner': 'someone',
        'amount': 5,
        'users': [['someone else', 5]],
        'group_id': 'invalid uuid'
    }
    test_expense_valid = db['expenses'].insert_one(input_expense_valid).inserted_id
    test_expense_invalid = db['expenses'].insert_one(input_expense_invalid).inserted_id
    # everything from here on until the item deletion in a try catch so
    # that if an error occurs the items still get deleted
    try:
        # the returned user and the expected result
        actual_valid = mongo.query_table('expenses', {'_id': test_expense_valid})
        actual_invalid = mongo.query_table('expenses', {'_id': test_expense_invalid})
        expected_valid = input_expense_valid
        expected_invalid = None
        # verifying correctness
        if not actual_valid == expected_valid and actual_invalid == expected_invalid:
            print('QUERY_USER FAILURE')
            if actual_valid != expected_valid:
                print('actual:')
                print(actual_valid)
                print('expected')
                print(expected_valid)
            else:
                print('invalid is null: ' + str(actual_invalid is None))
        else:
            print('query_user success')
    # if an error occurs print stack trace
    except Exception as e:
        print('uh oh you got an error')
        try:
            traceback.print_exc(e)
        except:
            print('?')
    # delete inserted test items
    db['groups'].delete_one({'_id': temp_group})
    if not actual_valid is None:
        db['expenses'].delete_one({'_id': test_expense_valid})
    if not actual_invalid is None:
        db['expenses'].delete_one({'_id': test_expense_invalid})

def query_notification_test():
    obj = mongo.query_table('groups', {'_id': 'something'})
    print(obj)

def query_pending_test():
    obj = mongo.query_table('pending_paid_expense', {'_id': 'something'})
    print(obj)

main()