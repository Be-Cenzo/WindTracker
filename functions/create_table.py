import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamodb.create_table(
    TableName = 'WindData',
    KeySchema = [
        {
            'AttributeName': 'uuid',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'timestamp',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions = [
        {
            'AttributeName': 'uuid',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'timestamp',
            'AttributeType': 'N'
        }
    ],
    ProvisionedThroughput = {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)