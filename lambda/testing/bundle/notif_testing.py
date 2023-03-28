import sys
import traceback
# change to absolute path on local machine
sys.path.append('C:\\Users\\rdrit\\OneDrive\\Documents\\GitHub\\BillMates-backend\\lambda\\python\\bundle')
import mongo
from bson import ObjectId
from pymongo import MongoClient
import notification as notif

def main():
    db = mongo.get_database()
    user = mongo.query_table('users', {'email': 'rdrittner@gmail.com'}, db)
    notif.make_notification('rdrittner@gmail.com', 'this is the message', 'this is the time')

main()