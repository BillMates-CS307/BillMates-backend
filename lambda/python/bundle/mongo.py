from pymongo import MongoClient

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

def query_table(table_name, query: dict):
    db = get_database()
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

#   users: {
#       _id: ObjectID (K),
#       email: String (K),
#       password: String (for now),
#       groups: String[] or ObjectID[] (FK), -- must check groups
#       name: String,
#       settings: {notification: String},
#       notifications: ObjectID[] (FK), -- must check notifications
#       all_expenses: ObjectID[] (FK) -- must check expenses  
#   }
def clean_up_user(user, db):
    expenses = list(db['expenses'].find())
    groups = list(db['groups'].find())
    notifs = list(db['notifications'].find())
    user['expenses'] = lazy_delete(user['expenses'], expenses, '_id')
    user['groups'] = lazy_delete(user['groups'], groups, 'uuid') # could be _id
    user['notifications'] = lazy_delete(user['notifications'], notifs, '_id')
    return user

#   groups: {
#       _id: ObjectID (K),
#       uuid: String (K),
#       name: String
#       members: (ObjectID or String (FK), int (balance))[], -- must check users
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
    user_list = []
    for t in group['members']:
        user_list.add(t[0])
    user_list = lazy_delete(user_list, users, 'email') # could be _id
    for i in range(0, len(group['members']) - 1):
        group['members'][i][0] = user_list[i]
    group['expenses'] = lazy_delete(group['expenses'], expenses, '_id')
    group['pending_payments'] = lazy_delete(group['pending_payments'], pending_payments, '_id')
    return group

#   expenses: {
#       _id: ObjectID (K),
#       owner: ObjectID or String (FK), -- *
#       users: (ObjectID or String, int (amount))[], (FK) -- *
#       group_id: ObjectID or String (FK), -- *
#       title: String,
#       amount: int
#   }
# *how should we handle the users or group associated to an expense being deleted?
def clean_up_expense(expense, db):
    # see *
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
    user_list = [notif['user']]
    user_list = lazy_delete(user_list, users, 'email') # could be _id
    if len(user_list) == 0:
        db['notifications'].delete_one({'_id': notif['_id']})
        notif = None
    return notif

#   pending_paid_expenses: {
#       _id: ObjectID (K)
#       original_id: ObjectID (FK, kind of)
#       group_id: ObjectID or String (FK) -- *
#       paid_to: ObjectID or String (FK) -- *
#       paid_by: ObjectID or String (FK -- *
#       amount: int
#   }
# *see asterisk in clean_up_expense
def clean_up_pending(user, db):
    # see *
    return user

def lazy_delete(working_list, ref_list, key_field):
    for f_key in working_list:
        exists = False
        for ref in ref_list:
            if ref[key_field] == f_key:
                exists = True
        if not exists:
            working_list.remove(f_key)
    return working_list