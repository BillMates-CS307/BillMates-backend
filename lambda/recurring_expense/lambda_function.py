import json
from pymongo import MongoClient
import bundle.g_password
import bundle.mongo as mongo
import bundle.api as api
from bson.objectid import ObjectId
import bundle.send as mail
import bundle.notification as notif
import datetime
import boto3

def lambda_handler(event, context):
    
    token = event['headers']['token']
    payload = json.loads(event['body'])
    response = {}
    
    # token verification
    response['token_success'] = api.check_token(token)
    
    if response['token_success']:
        parameters = json.loads(event['body'])
        start_date = parameters['start_date']
        start_time = parameters['start_time']
        freq = parameters['frequency']
        title = parameters['title'] # title of expense 
        total = parameters['total'] 
        comment = parameters['comment']
        group_id = parameters['group_id'] # group_id for expense
        owner_email = parameters['owner']
        u_expenses = parameters['expense'] # dict of form { 'email_of_user' : amount_owed }
        body = {
            'title': title,
            'total': total,
            'comment': comment,
            'group_id': group_id,
            'owner': owner_email,
            'expenses': u_expenses
        }
        header = {
            'token': token
        }
        
        # create cron rule
        # Parse start_date and start_time into datetime objects
        start_datetime = datetime.datetime.fromisoformat(start_date + 'T' + start_time)

        # Determine the minute and hour from the start time
        minute = start_datetime.minute
        hour = start_datetime.hour
    
        # Determine the day of the month and week from the start date
        day = start_datetime.day
        week_day = start_datetime.isoweekday()
    
        # Determine the month from the start date
        month = start_datetime.month
        # Create the cron expression based on the frequency
        if freq == 'daily':
            cron_rule = f"{minute} {hour} * * ? *"
        elif freq == 'weekly':
            cron_rule = f"{minute} {hour} ? * {week_day} *"
        elif freq == 'monthly':
            cron_rule = f"{minute} {hour} {day} * ? *"
        else:
            response['submit_success'] = False
            return api.build_capsule(response)
        print(cron_rule)
        
        # Set the schedule for the event rule to trigger every week
        schedule_expression = 'cron(' + cron_rule + ')'
        
        # Set the JSON payload that will be passed to the Lambda function
        recurring_payload = {
            'body': body,
            'headers': header
        }

        # Set the ARN of the Lambda function to be triggered by the event rule
        target_lambda_arn = 'arn:aws:lambda:us-east-2:615430537458:function:new_expense'

        # Create a CloudWatch Events client
        events_client = boto3.client('events')

        # Create the event rule that triggers the target Lambda function every week
        aws_response = events_client.put_rule(
            Name='recurring_expense_test',
            ScheduleExpression=schedule_expression,
            State='ENABLED',
            Description='This should create a new expense every week',
            EventBusName='default'
        )
    
        # Add the target Lambda function to the event rule
        events_client.put_targets(
            Rule='recurring_expense_test',
            Targets=[
                {
                    'Id': 'new_expense',
                    'Arn': target_lambda_arn,
                    'Input': json.dumps(recurring_payload)
                }
            ]
        )
    

    
        
    return api.build_capsule(response)

