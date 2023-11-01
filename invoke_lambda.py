import boto3

client = boto3.client('lambda')

response = client.invoke(
    FunctionName='DailyChargesFunction',
    Payload='{"key1": "value1", "key2": "value2"}'
)

print(response['Payload'].read())
