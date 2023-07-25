import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import os
import json

def lambda_handler(event, context):
    endpoint = f"http://{os.environ.get('LOCALSTACK_HOSTNAME')}:{os.environ.get('EDGE_PORT')}"
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2', endpoint_url=endpoint)

    table = dynamodb.Table('LatestData')
    sensor = json.loads(event['body'])
    table.put_item(Item=sensor)

    return { 
        'statusCode' : 200,
        'body': {
            'sensors' : sensor
            },
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, GET'
        },
        'isBase64Encoded': 'false'
    }