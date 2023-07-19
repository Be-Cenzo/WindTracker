import logging
import boto3
from botocore.exceptions import ClientError
import json
import logging

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    for record in event['Records']:
        payload = json.loads(record["body"])
        table = dynamodb.Table('WindData')
        latest = dynamodb.Table('LatestData')
        data={'uuid': payload['uuid'], 'name': payload['name'], 'createdAt': payload['createdAt'], 'windSpeed': payload['windSpeed'], 'windDirection': payload['windDirection']}
        table.put_item(Item=data)
        latest.update_item(
                Key={'name': payload["name"], 'createdAt': payload['sensorCreatedAt']},
                UpdateExpression="set windSpeed=:ws, windDirection=:wd, lastUpdated=:lu",
                ExpressionAttributeValues={
                    ':ws': payload['windSpeed'], ':wd': payload['windDirection'], ':lu': payload['createdAt']},
                ReturnValues="UPDATED_NEW")