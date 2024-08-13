import boto3
import os

dynamodb = boto3.resource('dynamodb', endpoint_url=f"http://{os.environ.get('LOCALSTACK_HOSTNAME')}:{os.environ.get('EDGE_PORT')}")

table = dynamodb.create_table(
    TableName = 'WindData',
    KeySchema = [
        {
            'AttributeName': 'sensorName',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'createdAt',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions = [
        {
            'AttributeName': 'sensorName',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'createdAt',
            'AttributeType': 'N'
        }
    ],
    ProvisionedThroughput = {
        'ReadCapacityUnits': 100,
        'WriteCapacityUnits': 100
    }
)

table = dynamodb.create_table(
    TableName = 'LatestData',
    KeySchema = [
        {
            'AttributeName': 'sensorName',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'createdAt',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions = [
        {
            'AttributeName': 'sensorName',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'createdAt',
            'AttributeType': 'N'
        }
    ],
    ProvisionedThroughput = {
        'ReadCapacityUnits': 100,
        'WriteCapacityUnits': 100
    }
)

print("Tables created!")
