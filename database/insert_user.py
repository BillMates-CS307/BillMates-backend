# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database

# TODO: should type the param to pretend the error
def insert_user(user_data: dict):
  dbname = get_database()
  users = dbname["users"]

  # TODO: need function to verify that user_data has proper properties before call this fn
  users.insert_one(user_data)
