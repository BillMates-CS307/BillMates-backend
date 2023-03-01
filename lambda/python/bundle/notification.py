
from mongo import get_database
from bson.objectid import ObjectId

def make_notification(user_email: str, message: str, time: str):
    db = get_database()
    notifs = db['notifications']
    users = db['users']
    new_notif = {
        'sender' : 'BillMates',
        'message': message,
        'time': time,
        'isread': False
    }
    user = users.find_one({'email':user_email})
    id = notifs.insert_one(new_notif)
    users.update_one(user, {"$set": { "notifications": user['notifications'] + [ObjectId(id.inserted_id)]} })
