import json
from pymongo import MongoClient
import bundle.g_password
import bundle.mongo as mongo
import bundle.api as api
from bson.objectid import ObjectId
import bundle.send as mail
import bundle.notification as notif
import datetime
from datetime import timedelta
import boto3
import uuid as uu

def lambda_handler(event, context):
    
    token = event['headers']['token']
    payload = json.loads(event['body'])
    response = {}
    
    # token verification
    response['token_success'] = api.check_token(token)
    
    if response['token_success']:
        db = mongo.get_database()
        # retrieve parameters
        parameters = json.loads(event['body'])
        start_date = parameters['start_date']
        start_time = parameters['start_time']
        freq = parameters['frequency']
        title = parameters['title'] 
        total = parameters['total'] 
        comment = parameters['comment']
        group_id = parameters['group_id']
        owner_email = parameters['owner']
        u_expenses = parameters['expense']
        tag = parameters['tag']
        # get calendar
        cal = mongo.query_table('calendars', {'group_id': group_id}, db)
        if cal is None:
            response['submit_success'] = False
            return api.build_capsule(response)
        response['submit_success'] = True
        
        body = { # for eventrule payload
            'title': title,
            'total': total,
            'comment': comment,
            'group_id': group_id,
            'owner': owner_email,
            'expense': u_expenses,
            'tag': tag
        }
        header = {
            'token': token
        }
        
        cal_entry = { # for calendar entry
            'name': title,
            'total': total,
            'description': comment,
            'creator': owner_email,
            'expense': u_expenses,
            'frequency': freq,
            'date': start_date,
            'time': start_time
        }

        
        # create cron rule
        # Parse start_date and start_time into datetime objects
        start_datetime = datetime.datetime.fromisoformat(start_date + 'T' + start_time)
        # aws is 4 hours ahead so add 4 hours
        start_datetime = start_datetime + timedelta(hours=4)
        
        # Determine the minute and hour, day of month, and month from the start time
        minute = start_datetime.minute
        hour = start_datetime.hour
        day = start_datetime.day
        month = start_datetime.month # doesn't actually get used
        
        # get day of week, aws uses sunday as day 1 while datetime library uses monday as day 1
        week_day = (start_datetime.isoweekday() % 7) + 1
        
        # Create the cron expression based on the frequency
        # minute hour day_of_month month day_of_week year 
        if freq == 'daily':
            cron_rule = f"{minute} {hour} * * ? *"
        elif freq == 'weekly':
            cron_rule = f"{minute} {hour} ? * {week_day} *"
        elif freq == 'monthly':
            cron_rule = f"{minute} {hour} {day} * ? *"
        else:
            response['submit_success'] = False
            return api.build_capsule(response)
        
        # create unique eventrule name
        rule_name = str(uu.uuid4())
        cal_entry['recurring_expense_id'] = rule_name
        
        # Set the schedule for the event rule to trigger every week
        schedule_expression = 'cron(' + cron_rule + ')'
        
        # Set the JSON payload that will be passed to the Lambda function
        # Currently doesn't work
        recurring_payload = {
            'body': body,
            'headers': header
        }

        # Create a CloudWatch Events client and lambda client
        events_client = boto3.client('events')
        lambda_client = boto3.client('lambda')
        
        # Set the name and ARN of the Lambda function to be triggered by the event rule (new_expense)
        function_name = 'new_expense'
        function_arn = 'arn:aws:lambda:us-east-2:615430537458:function:new_expense'

        # Create the event rule that triggers new_expense every day/week/month
        aws_response = events_client.put_rule(
            Name=rule_name,
            ScheduleExpression=schedule_expression,
            State='ENABLED',
            Description=title,
            EventBusName='default'
        )
        
        if 'RuleArn' not in aws_response: # check for failure
            response['submit_success'] = False
            response['ERROR'] = aws_response
            return api.build_capsule(response)
    
        # Add new_expense to the event rule as the target
        events_client.put_targets(
            Rule=rule_name,
            Targets=[
                {
                    'Id': function_name,
                    'Arn': function_arn,
                    'Input': json.dumps(recurring_payload)
                }
            ]
        )
        
        # Add trigger to new_expense for the eventrule
        lambda_client.add_permission(
            FunctionName=function_name,
            StatementId=rule_name,
            Action='lambda:InvokeFunction',
            Principal='events.amazonaws.com',
            SourceArn=aws_response['RuleArn']
        )
        
        # add cal_entry to the calendar
        cal['recurring_expenses'].append(cal_entry)
        db['calendars'].update_one({'group_id': group_id}, {'$set': {'recurring_expenses': cal['recurring_expenses']}})

    return api.build_capsule(response)

