
from bundle.mongo import get_database
from bundle.mongo import query_table
from bson.objectid import ObjectId

def make_notification(user_email: str, message: str, time: str):
    db = get_database()
    notifs = db['notifications']
    user = query_table('users', {'email':user_email}, db)
    users = db['users']
    new_notif = {
        'user' : user['email'],
        'sender' : 'BillMates',
        'message': message,
        'time': time,
        'isread': False
    }
    id = notifs.insert_one(new_notif)
    users.update_one(user, {"$set": { "notifications": user['notifications'] + [ObjectId(id.inserted_id)]} })
