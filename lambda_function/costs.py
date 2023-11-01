import boto3
import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Initialize a session using Amazon Cost Explorer
    client = boto3.client('ce')

    # Define the time period for the last 7 days
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(3)).strftime('%Y-%m-%d')

    # Retrieve the cost and usage data
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='DAILY',
        Metrics=['BlendedCost']
    )

    # Modify the amounts to have only two decimal places
    for result in response['ResultsByTime']:
        amount = result['Total']['BlendedCost']['Amount']
        result['Total']['BlendedCost']['Amount'] = "{:.2f}".format(float(amount))
    
    # Send the data as a message to SNS
    send_sns_message(response)

def format_cost_data(response):
    formatted_message = "Daily AWS Charges:\n\n"
    
    for result in response['ResultsByTime']:
        start_date = result['TimePeriod']['Start']
        end_date = result['TimePeriod']['End']
        amount = result['Total']['BlendedCost']['Amount']
        unit = result['Total']['BlendedCost']['Unit']
        
        formatted_message += f"From {start_date} to {end_date}: {amount} {unit}\n"
    
    return formatted_message

def send_sns_message(response):
    sns_client = boto3.client('sns')
    topic_arn = "arn:aws:sns:us-east-1:773465154107:DailyChargesTopic"  # Replace with your SNS Topic ARN
    
    # Compute the total for the last 3 days
    total_cost = sum(float(result['Total']['BlendedCost']['Amount']) for result in response['ResultsByTime'])
    
    # Subject with running total
    subject = f"AWS DAILY SPEND SUMMARY - 3 Day Total: ${total_cost:.2f} USD"

    # Format the message
    formatted_content = format_cost_data(response)
    
    sns_client.publish(TopicArn=topic_arn, Message=formatted_content, Subject=subject)
