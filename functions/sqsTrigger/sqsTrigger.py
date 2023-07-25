import logging
import boto3
from botocore.exceptions import ClientError
import json
import logging
import os

def lambda_handler(event, context):
    endpoint = f"http://{os.environ.get('LOCALSTACK_HOSTNAME')}:{os.environ.get('EDGE_PORT')}"
    dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint)

    for record in event['Records']:
        payload = json.loads(record["body"])
        table = dynamodb.Table('WindData')
        latest = dynamodb.Table('LatestData')
        data={'uuid': payload['uuid'], 'sensorName': payload['sensorName'], 'createdAt': payload['lastUpdated'], 'windSpeed': payload['windSpeed'], 'windDirection': payload['windDirection'], 'error': payload['error']}
        table.put_item(Item=data)
        latest.update_item(
                Key={'sensorName': payload["sensorName"], 'createdAt': payload['createdAt']},
                UpdateExpression="set windSpeed=:ws, windDirection=:wd, lastUpdated=:lu",
                ExpressionAttributeValues={
                    ':ws': payload['windSpeed'], ':wd': payload['windDirection'], ':lu': payload['lastUpdated']},
                ReturnValues="UPDATED_NEW")