from random import randrange
import random
from sensors import Sensor
import sys
import time
import threading
import boto3
import json
import datetime
import uuid

class Factory:
    def __init__(self, name, sensorNum):
        self.name = name
        self.sensorNum = sensorNum
        self.startLatitude = 40.853294
        self.startLongitude = 14.305573
        self.sensors = []
        self.createSensors()
        self.subscribeToInfrastracture()
    
    def createSensors(self):
        for i in range(self.sensorNum):
            lat = self.startLatitude + random.uniform(0, 0.2)
            lng = self.startLongitude + random.uniform(-0.125, 0.125)
            sensor = Sensor(f"Sensor{i}", lat, lng)
            self.sensors.append(sensor)
    
    def subscribeToInfrastracture(self):
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
        table = dynamodb.Table('Sensors')
        latest = dynamodb.Table('LatestData')
        for i in range(self.sensorNum):
            item = self.sensors[i].getSignature()
            id = str(uuid.uuid4())
            item.update({"uuid": id})
            response = table.put_item(
                Item = item
            )
            data = {
                "windSpeed": self.sensors[i].getWindSpeed(),
                "windDirection": self.sensors[i].getWindSpeed(),
                "name": item["name"],
                "createdAt": item["createdAt"],
                "lastUpdated": item["createdAt"]
            }
            response = latest.put_item(
                Item = data
            )
            print(data)
    
    def printAll(self):
        for i in range(self.sensorNum):
            print(f"Sensore: {self.sensors[i].getName()}")
            print(f"Velocità del vento: {self.sensors[i].getValue()[0]}km/h")
            print(f"Direzione del vento: {self.sensors[i].getValue()[1]}")
            print(f"Latitude: {self.sensors[i].getLatitude()} Longitude: {self.sensors[i].getLongitude()}")
    
    def updateValues(self, event, updateTime):
        while True:
            for i in range(self.sensorNum):
                self.sensors[i].updateWindSpeed()
                self.sensors[i].updateWindDirection()
            time.sleep(updateTime)
            self.postToQueue()
            if event.is_set():
                break

    def postToQueue(self):
        sqs = boto3.client('sqs', aws_access_key_id=None, aws_secret_access_key=None, endpoint_url='http://localhost:4566')
        for i in range(self.sensorNum):
            msg = self.sensors[i].getMessage()
            id = str(uuid.uuid4())
            time = int(datetime.datetime.now().timestamp())
            msg.update({"uuid": id, "createdAt": time, "sensorCreatedAt": int(self.sensors[i].getCreatedAt())})
            print(msg)
            postMessageToQueue(msg, sqs)

def postMessageToQueue(message, sqsClient):
    queue_url = 'http://localhost:4566/000000000000/sqs_queue'
    resp = sqsClient.send_message(
        QueueUrl=queue_url,
        MessageBody=(
            json.dumps(message)
        )
    )
    print(resp['MessageId'])


num = int(sys.argv[1])
update = int(sys.argv[2])
duration = int(sys.argv[3])
factory = Factory("Factory", num)
factory.postToQueue()
event = threading.Event()

thread1 = threading.Thread(name='h1', target=factory.updateValues, args=(event, update))
thread1.start()
time.sleep(duration)

event.set()