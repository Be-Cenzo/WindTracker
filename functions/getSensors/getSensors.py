import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    table = dynamodb.Table('Sensors')
    response = table.scan()
    data = response["Items"]
    
    return { 
        'statusCode' : 200,
        'body': {
            'sensors' : data
            },
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }