import sys
sys.path.append('C:\\Users\\rdrit\\OneDrive\\Documents\\GitHub\\BillMates-backend\\lambda\\python\\bundle')
import mongo

def main():
    query_table_test()


def query_table_test():
    obj = mongo.query_table('users', {'email': 'lcover@purdue.edu'})
    print(obj)

main()