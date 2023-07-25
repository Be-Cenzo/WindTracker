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
        self.topic_arn = ""
        self.getTopicArn()
        self.subscribeToInfrastracture()
    
    def createSensors(self):
        for i in range(self.sensorNum):
            lat = self.startLatitude + random.uniform(0, 0.2)
            lng = self.startLongitude + random.uniform(-0.125, 0.125)
            sensor = Sensor(f"Sensor{i}", lat, lng)
            self.sensors.append(sensor)

    def getTopicArn(self):
        sns = boto3.client('sns', endpoint_url='http://localhost:4566')
        all_topics = sns.list_topics()
        all_topics = all_topics["Topics"]
        for topic in all_topics:
            arn = topic["TopicArn"] 
            attr = sns.get_topic_attributes(
                TopicArn=arn
            )
            name = attr["Attributes"]["DisplayName"]
            if(name == "errors-topic"):
                self.topic_arn = arn
                break
    
    def subscribeToInfrastracture(self):
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
        table = dynamodb.Table('Sensors')
        latest = dynamodb.Table('LatestData')
        for i in range(self.sensorNum):            
            self.sensors[i].subscribeToInfrastracture()
    
    def printAll(self):
        for i in range(self.sensorNum):
            print(f"Sensore: {self.sensors[i].getName()}")
            print(f"Velocità del vento: {self.sensors[i].getValue()[0]}km/h")
            print(f"Direzione del vento: {self.sensors[i].getValue()[1]}")
            print(f"Latitude: {self.sensors[i].getLatitude()} Longitude: {self.sensors[i].getLongitude()}")
    
    def updateValues(self, toggleUpdate, stopUpdate, updateTime):
        while True:
            if stopUpdate.is_set():
                break
            while True:
                if toggleUpdate.is_set() or stopUpdate.is_set():
                    break
                time.sleep(updateTime)
                for i in range(self.sensorNum):
                    if not self.sensors[i].isError():
                        self.sensors[i].updateWindSpeed()
                        self.sensors[i].updateWindDirection()
                        self.sensors[i].updateError()
                        if self.sensors[i].isError():
                            self.sensors[i].postToTopic(self.topic_arn, self.sensors[i].getSignature(), "Errore nel sensore!")
                    self.postToQueue()

    def postToQueue(self):
        sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')
        for i in range(self.sensorNum):
            if not self.sensors[i].isError():
                msg = self.sensors[i].getMessage()
                id = str(uuid.uuid4())
                time = int(datetime.datetime.now().timestamp())
                msg.update({"uuid": id})
                #print(msg)
                postMessageToQueue(msg, sqs)

    def fixSensor(self, pos):
        self.sensors[pos].fixSensor()

def postMessageToQueue(message, sqs_client):
    queue_url = 'http://localhost:4566/000000000000/sqs_queue'
    resp = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=(
            json.dumps(message)
        )
    )

def prova(e, x):
    while True :
        x.updateWindSpeed()
        if e.is_set():
            break

num = int(sys.argv[1])
update = int(sys.argv[2])
duration = int(sys.argv[3])

factory = Factory("Factory", num)
factory.postToQueue()

toggleUpdate = threading.Event()
toggleUpdate.set()
stopUpdate = threading.Event()

updater = threading.Thread(name='h1', target=factory.updateValues, args=(toggleUpdate, stopUpdate, update))
updater.start()

while True :
    print("Insert:\n - 'start' to start updating values\n - 'stop' to stop updating values\n - 'fix' to fix a sensor\n - 'exit' - to close program")
    y = input()
    if y == "stop" :
        if not toggleUpdate.is_set():
            toggleUpdate.set()
        print("Stopped")
    if y == "start" :
        if toggleUpdate.is_set():
            toggleUpdate.clear()
        print("Started updating values")
    if y == "fix":
        print("Which component is fixed?")
        pos = input()
        factory.fixSensor(int(pos))
    if y == "exit" :
        stopUpdate.set()
        break