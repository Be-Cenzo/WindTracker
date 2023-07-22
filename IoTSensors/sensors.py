import sys
from random import randrange
import time
import datetime
import threading
import boto3
import json

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
        self.windSpeed = self.windSpeed+(randrange(10)*self.casuality*minus)
    
    def updateWindDirection(self):
        if (randrange(10)/10) > self.changeDirectionThreshold:
            self.windDirection = self.directions[randrange(8)]
    
    def updateError(self):
        if (randrange(100)/100) >= self.errorThreshold:
            print("Error True")
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
            "createdAt": int(self.createdAt)
        }
        return message
    
    def postToTopic(self, topic_arn, message, subject):
        sns_resource = boto3.client('sns', endpoint_url='http://localhost:4566')
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
        
"""
print(f"Arguments count: {len(sys.argv)}")
s = Sensor("prova", 0, 0)
print(f"Velocità del vento: {s.getValue()[0]}km/h")
print(f"Direzione del vento: {s.getValue()[1]}")

event = threading.Event()

thread1 = threading.Thread(name='h1', target=automaticUpdate, args=(s, event))
thread1.start()
time.sleep(1.5)

print(f"Velocità del vento: {s.getValue()[0]}km/h")
print(f"Direzione del vento: {s.getValue()[1]}")

event.set()
"""