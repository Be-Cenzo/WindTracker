import boto3


def load_movies():
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    table = dynamodb.Table('WindData')
    response = table.scan()
    data = response["Items"]
    print(data)
    for i in data:
        print(i)

load_movies()