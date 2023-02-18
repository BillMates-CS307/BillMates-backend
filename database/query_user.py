# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database

def query_user(user_data: dict):
  dbname = get_database()

  # Create a new collection
  users = dbname["users"]

  user = users.find_one({'username': user_data.username, 'password': user_data.password})

  # TODO: should return to client
  print(user)
