from pymongo import MongoClient
from copy import deepcopy

analytic_temp = {
    "month" : {
                    "january": 0,
                    "february": 0,
                    "march": 0,
                    "april" : 0,
                    "june" : 0,
                    "july" : 0,
                    "august" : 0,
                    "september": 0,
                    "october" : 0,
                    "november" : 0,
                    "december" : 0
                },
    "tags" : {
        "Entertainment": 0, "Rent": 0, "Food": 0, "Misc": 0, "No Tag" : 0
    }
        
}

def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://biocle8339:LF29bzT9agnpGJHm@cluster0.r7oohad.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['billmates']

def query_user(user_data: dict, get_collection: bool):
    dbname = get_database()

    # Create a new collection
    users = dbname["users"]

    # user_date = {'email': ___ , 'password': ____}
    user = users.find_one(user_data)

    # TODO: should return to client
    if not get_collection:
        return user
    return (user, users)

# calculates user balance in a given group
# parameters: user_id (string or ObjectId)
#             group_id (string or ObjectId)
#             db (database from get_database())
# returns double (only negative if user not found in group's user field)
# do not call this if the the database has been modified since retrieving group object
# only way to store balance in db that wouldn't be problematic would be to make another
def user_balance_in_group(user_id, group_id, db):
    expenses = list(db['expenses'].find())
    user_group_balance = 0
    for e in expenses:
        if e['group_id'] == group_id:
            if e['owner'] == user_id:
                for u in e['users']:
                    user_group_balance += u[1]
            else:
                if query_table('users', {'email' : e['owner']}, db) != None:
                    for u in e['users']:
                        if u[0] == user_id:
                            user_group_balance -= u[1]
    if db['groups'].find_one({'uuid' : group_id})['archived']:
        user_group_balance = 0
    return user_group_balance

# Simple getter to grab group name from group_id (primarily for get_user)
def get_group_name(group_id: str, db):
    return db['groups'].find_one({'uuid' : group_id})['name']


# name of table being queried on, query, database from get_database()
def query_table(table_name, query: dict, db):
    table = db[table_name]
    out = table.find_one(query)
    if out is None:
        return None
    if table_name == 'users':
        out = clean_up_user(out, db)
    elif table_name == 'groups':
        out = clean_up_group(out, db)
    elif table_name == 'expenses':
        out = clean_up_expense(out, db)
    elif table_name == 'notifications': 
        out = clean_up_notification(out, db)
    elif table_name == 'pending_paid_expenses':
        out = clean_up_pending(out, db)
    return out

# values defining keys for tables with multiple options
user_key = 'email'
group_key = 'uuid'

#   users: {
#       _id: ObjectID (K),
#       email: String (K),
#       password: String (for now),
#       groups: String[] or ObjectID[] (FK), -- must check groups
#       name: String,
#       settings: {notification: String},
#       notifications: ObjectID[] (FK), -- must check notifications
#       expenses: ObjectID[] (FK) -- must check expenses  
#   }
def clean_up_user(user, db):
    expenses = list(db['expenses'].find())
    groups = list(db['groups'].find())
    notifs = list(db['notifications'].find())
    user['expenses'] = lazy_delete(user, 'expenses', 'users', user_key, expenses, '_id', db)
    user['groups'] = lazy_delete(user, 'groups', 'users', user_key, groups, group_key, db) # user_key is email, group_key is uuid
    user['notifications'] = lazy_delete(user, 'notifications', 'users', user_key, notifs, '_id', db)
    return user

#   groups: {
#       _id: ObjectID (K),
#       uuid: String (K),
#       name: String
#       members: (ObjectID or String (FK)[], -- must check users
#       expenses: ObjectID[] (FK), -- must check expenses
#       pending_payments: ObjectID[] (FK) -- must check pending_payments
#       manager: ObjectID or String (FK), -- what to do if manager deletes account?
#       calendar: ObjectID (FK), -- implement later
#       shopping_list: ObjectID (FK) -- implement later
#   }
def clean_up_group(group, db):
    users = list(db['users'].find())
    expenses = list(db['expenses'].find())
    pending_payments = list(db['pending_paid_expenses'].find())
    group['members'] = lazy_delete(group, 'members', 'groups', group_key, users, user_key, db) # group_key is uuid, user_key is email
    group['expenses'] = lazy_delete(group, 'expenses', 'groups', group_key, expenses, '_id', db)
    group['pending_payments'] = lazy_delete(group, 'pending_payments', 'groups', group_key, pending_payments, '_id', db)
    return group

#   expenses: {
#       _id: ObjectID (K),
#       owner: ObjectID or String (FK), -- *
#       users: (ObjectID or String, int (amount))[], (FK) -- *
#       group_id: ObjectID or String (FK), -- delete expense if group deleted
#       title: String,
#       amount: int
#   }
# *how should we handle the users associated to an expense being deleted?
def clean_up_expense(expense, db):
    groups = list(db['groups'].find())
    # scuffed but should work
    obj = {'list': [expense['group_id']]}
    group_list = lazy_delete(obj, 'list', '', '', groups, group_key, db, update=False) # group_key is uuid
    if len(group_list) == 0:
        db['expenses'].delete_one({'_id': expense['_id']})
        expense = None
    return expense

#   notification: {
#       _id: ObjectID (K),
#       user: ObjectID or String (FK), -- delete notif if user is deleted
#       sender: String,
#       time: String,
#       message: String,
#       isRead: boolean   
#   }
def clean_up_notification(notif, db):
    users = list(db['users'].find())
    # scuffed but should work
    obj = {'list': [notif['user']]}
    user_list = lazy_delete(obj, 'list', '', '', users, user_key, db, update=False) # user_key is email
    if len(user_list) == 0:
        db['notifications'].delete_one({'_id': notif['_id']})
        notif = None
    return notif

#   pending_paid_expenses: {
#       _id: ObjectID (K)
#       original_id: ObjectID (FK, kind of)
#       group_id: ObjectID or String (FK) -- delete pending payment if group deleted
#       paid_to: ObjectID or String (FK) -- *
#       paid_by: ObjectID or String (FK -- *
#       amount: int
#   }
# *see asterisk in clean_up_expense
def clean_up_pending(pending, db):
    groups = list(db['groups'].find())
    # scuffed but should work
    obj = {'list': [pending['group_id']]}
    group_list = lazy_delete(obj, 'list', '', '', groups, group_key, db, update=False) # group_key is uuid
    if len(group_list) == 0:
        db['pending_paid_expenses'].delete_one({'_id': pending['_id']})
        pending = None
    return pending
    
# object is local value of an item in collection table
# list_field is the field of object that is the list of foreign keys
# table is the table that is being worked on
# obj_key_field is the field of object that is its key
# ref_list is the list of local objects from a different table that the list in list_field is being compared to
# key_field is the field that cotains the keys of ref_list
# db is the database
# update is whether or not the working table gets updated in the database, default true
# set to false if the entire object must be deleted, not just a field of it
# if update is false, table and obj_key_field can be blank
def lazy_delete(object, list_field, table, obj_key_field, ref_list, key_field, db, update=True):
    working_list = object[list_field]
    working_list_copy = working_list.copy()
    changed = False
    new_val = {}
    for f_key in working_list:
        exists = False
        for ref in ref_list:
            if ref[key_field] == f_key:
                exists = True
        if not exists:
            changed = True
            working_list_copy.remove(f_key)
            if update:
                new_val = {list_field: working_list_copy}
    if changed and update:       
        db[table].update_one({obj_key_field: object[obj_key_field]}, {'$set': new_val})
    return working_list_copy

# Function to generate a new analytics object for MongoDB
def new_analytics():
    return deepcopy(analytic_temp)