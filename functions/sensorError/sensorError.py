import boto3
import json
import os

def lambda_handler(event, context):
    endpoint = f"http://{os.environ.get('LOCALSTACK_HOSTNAME')}:{os.environ.get('EDGE_PORT')}"
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2', endpoint_url=endpoint)

    for record in event['Records']:
        payload = json.loads(record["Sns"]["Message"])
        sensors = dynamodb.Table('Sensors')
        latest = dynamodb.Table('LatestData')
        latest.update_item(
                Key={'sensorName': payload["sensorName"], 'createdAt': payload['createdAt']},
                UpdateExpression="set #error=:er",
                ExpressionAttributeValues={
                    ':er': payload['error']},
                ExpressionAttributeNames= {"#error" : "error" },
                ReturnValues="UPDATED_NEW")

