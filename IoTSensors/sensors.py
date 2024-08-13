import sys
from random import randrange
import time
import datetime
import threading
import boto3
import json
import requests
import os

restfile = open("rest.json")
data = json.load(restfile)

restid = data["rest_api_id"]
restfile.close()

endpoint = f"http://{os.environ.get('LOCALSTACK_HOSTNAME')}:{os.environ.get('EDGE_PORT')}"
basePath = f"{endpoint}/restapis/{restid}/local/_user_request_/"

class Sensor:

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.casuality = 0.1
        self.changeDirectionThreshold = 0.8
        self.windSpeed = randrange(10)
        self.directions = ['S','SE', 'SO', 'E', 'O', 'N', 'NE', 'NO']
        self.windDirection = self.directions[randrange(8)]
        self.error = False
        self.errorThreshold = 0.95
        self.createdAt = datetime.datetime.now().timestamp()
    
    def getValue(self):
        return self.windSpeed, self.windDirection
    
    def getWindSpeed(self):
        return self.windSpeed
    
    def getWindDirection(self):
        return self.windDirection

    def getName(self):
        return self.name

    def getLatitude(self):
        return self.latitude
    
    def getLongitude(self):
        return self.longitude

    def isError(self):
        return self.error
    
    def getCreatedAt(self):
        return self.createdAt

    def setWindSpeed(self, windSpeed):
        self.windSpeed = setWindSpeed

    def setWindDirection(self, windDirection):
        self.windDirection = windDirection
    
    def updateWindSpeed(self):
        minus = 1
        if randrange(2) and self.windSpeed > 1:
            minus = -1
        self.windSpeed = round(self.windSpeed+(randrange(10)*self.casuality*minus), 2)
    
    def updateWindDirection(self):
        if (randrange(10)/10) > self.changeDirectionThreshold:
            self.windDirection = self.directions[randrange(8)]
    
    def updateError(self):
        if (randrange(100)/100) >= self.errorThreshold:
            print(f"{self.name} error occured")
            self.error = True

    
    def getSignature(self):
        item = {
            "sensorName": self.name,
            "latitude": str(self.latitude),
            "longitude": str(self.longitude),
            "error": self.error,
            "createdAt": int(self.createdAt)
        }
        return item
    
    def getMessage(self):
        message = {
            "sensorName": self.name,
            "latitude": str(self.latitude),
            "longitude": str(self.longitude),
            "windSpeed": str(self.windSpeed),
            "windDirection": self.windDirection,
            "error": self.error,
            "createdAt": int(self.createdAt),
            "lastUpdated": int(datetime.datetime.now().timestamp())
        }
        return message
    
    def subscribeToInfrastracture(self):
        data = self.getMessage()
        data["lastUpdated"] = data["createdAt"]
        x = requests.post(f"{basePath}subscribeSensor", json = data)
    
    def fixSensor(self):
        self.error = False
        data = self.getMessage()
        x = requests.post(f"{basePath}fixSensor", json = data)
        print("Fixed")

    
    def postToTopic(self, topic_arn, message, subject):
        sns_resource = boto3.client('sns', endpoint_url=endpoint)
        response = sns_resource.publish(
            TopicArn=topic_arn,
            Message=json.dumps({'default':json.dumps(message)}),
            Subject=subject,
            MessageStructure='json',
        )

        
def automaticUpdate(sensor, event):
    while True:
        sensor.updateWindSpeed()
        sensor.updateWindDirection()
        time.sleep(1)
        if event.is_set():
            break