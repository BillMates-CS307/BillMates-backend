import pymongo

client = pymongo.MongoClient("mongodb+srv://benlilley:RhzVtsgixh2sZvwN@cluster0.r7oohad.mongodb.net/?retryWrites=true&w=majority")
db = client.test_database
collection = db.users.find_one()
print(collection)