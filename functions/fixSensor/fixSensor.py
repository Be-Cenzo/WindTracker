import boto3
import json
import os

def lambda_handler(event, context):
    endpoint = f"http://{os.environ.get('LOCALSTACK_HOSTNAME')}:{os.environ.get('EDGE_PORT')}"
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2', endpoint_url=endpoint)

    table = dynamodb.Table('LatestData')
    sensor = json.loads(event['body'])
    table.update_item(
            Key={'sensorName': sensor['sensorName'], 'createdAt': sensor['createdAt']},
            UpdateExpression="set latitude=:lat, longitude=:lng, windSpeed=:ws, windDirection=:wd, lastUpdated=:lu, #error=:er",
            ExpressionAttributeValues={
                ':lat':sensor['latitude'], ':lng':sensor['longitude'], ':ws': sensor['windSpeed'], ':wd': sensor['windDirection'], ':lu': sensor['lastUpdated'], ':er': sensor['error']},
            ExpressionAttributeNames= {"#error" : "error" },
            ReturnValues="UPDATED_NEW")
    
    return { 
        'statusCode' : 200,
        'body': {},
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, GET'
        },
        'isBase64Encoded': 'false'
    }

