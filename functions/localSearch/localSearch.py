import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import os
import json

def lambda_handler(event, context):
    endpoint = f"http://{os.environ.get('LOCALSTACK_HOSTNAME')}:{os.environ.get('EDGE_PORT')}"
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2', endpoint_url=endpoint)

    table = dynamodb.Table('LatestData')
    #try:
    """
    response = table.query(Limit=1,
        ScanIndexForward=False,
        KeyConditionExpression="#name = :name",
        ExpressionAttributeValues={":name" : name},
        ExpressionAttributeNames= {"#name" : "name" }
    )
    """
    """
    except ClientError as err:
        return { 
            'statusCode' : 500,
            'body': {
                'sensors' : err 
                },
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }
    """
    sensors = json.loads(event['body'])
    sensors_list = sensors['sensors'] 
    res = []
    for s in sensors_list:
        response = table.get_item(
            Key={
                'sensorName': s['sensorName'],
                'createdAt': s['createdAt']
            }
        )
        if response['Item']:
            res.append(response['Item'])

    return { 
        'statusCode' : 200,
        'body': {
            'sensors' : res
            },
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, GET'
        },
        'isBase64Encoded': 'false'
    }