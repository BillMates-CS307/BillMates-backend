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
#       groups: String[] or ObjectID[] (FK) -- must check groups,
#       name: String,
#       settings: {notification: String},
#       notifications: ObjectID[] (FK) -- must check notifications,
#       all_expenses: ObjectID[] (FK) -- must check expenses  
#   }
def clean_up_user(user, db):
    expenses = list(db['expenses'].find())
    groups = list(db['groups'].find())
    notifs = list(db['notifications'].find())
    user = lazy_delete(user['expenses'], expenses, '_id')
    user = lazy_delete(user['groups'], groups, 'uuid')
    user = lazy_delete(user['notifications'], notifs, '_id')
    return user

def clean_up_group(user, db):
    return user

def clean_up_expense(user, db):
    return user

def clean_up_notification(user, db):
    return user

def clean_up_pending(user, db):
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