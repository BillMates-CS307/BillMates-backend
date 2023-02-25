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
