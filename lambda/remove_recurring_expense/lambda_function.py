import json
import bundle.api as api
from pymongo import MongoClient
import bundle.mongo as mongo
from bson.objectid import ObjectId
import datetime
import boto3

def lambda_handler(event, context):
    # Parameters
    payload = json.loads(event['body'])
    rule_name = payload['recurring_expense_id']
    group_id = payload['group_id']
    
    # Build reponse JSON
    response = {}

    # Verify token is correct before running more commands
    token = event['headers']['token']
    response["token_success"] = api.check_token(token)
    
    if response['token_success']:
        db = mongo.get_database()
        cal = mongo.query_table('calendars', {'group_id': group_id}, db)
        if cal is None:
            response['remove_success'] = False
            return api.build_capsule(response)
        recurs = cal['recurring_expenses']
        recur = {}
        for r in recurs:
            if r['recurring_expense_id'] == rule_name:
                recur = r
        if recur == {}:
            response['remove_success'] = False
            return api.build_capsule(response)
        response['remove_success'] = True
        recurs.remove(recur)
        
        event_client = boto3.client('events')
        rem_t_response = event_client.remove_targets(Rule=rule_name, Ids=['new_expense'])
        rem_rule_response = event_client.delete_rule(Name=rule_name)
        db['calendars'].update_one({'group_id': group_id}, {'$set': {'recurring_expenses': recurs}})
        
    return api.build_capsule(response)
