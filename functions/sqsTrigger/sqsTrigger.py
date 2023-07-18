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
        data={'uuid': payload['uuid'], 'name': payload['name'], 'latitude': payload['latitude'], 'longitude': payload['longitude'], 'timestamp': payload['timestamp'], 'windSpeed': payload['windSpeed'], 'windDirection': payload['windDirection']}
        #print("Adding movie: ", release_date, payload)
        #data = json.dumps(payload)
        table.put_item(Item=data)