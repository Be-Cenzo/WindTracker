import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    table = dynamodb.Table('LatestData')
    #name = str(event['queryStringParameters']['name'])
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