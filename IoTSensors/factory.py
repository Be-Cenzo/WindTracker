from random import randrange
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
        self.startLatitude = randrange(10)
        self.startLongitude = randrange(10)
        self.sensors = []
        self.createSensors()
    
    def createSensors(self):
        for i in range(self.sensorNum):
            sensor = Sensor(f"Sensor{i}", self.startLatitude + randrange(5), self.startLongitude + randrange(5))
            self.sensors.append(sensor)
    
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
        for i in range(self.sensorNum):
            msg = self.sensors[i].getMessage()
            id = str(uuid.uuid4())
            time = int(datetime.datetime.now().timestamp())
            msg.update({"uuid": id, "timestamp": time})
            print(msg)
            postMessageToQueue(msg)

def postMessageToQueue(message):
    sqs = boto3.client('sqs', aws_access_key_id=None, aws_secret_access_key=None, endpoint_url='http://localhost:4566')
    queue_url = 'http://localhost:4566/000000000000/sqs_queue'
    resp = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=(
            json.dumps(message)
        )
    )
    print(resp['MessageId'])

print(sys.argv[1])
num = int(sys.argv[1])
factory = Factory("Factory", num)
factory.postToQueue()

event = threading.Event()

thread1 = threading.Thread(name='h1', target=factory.updateValues, args=(event, 1))
thread1.start()
time.sleep(1.5)

event.set()