import sys
from random import randrange
import time
import datetime
import threading

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
    
    def getCreatedAt(self):
        return self.createdAt

    def setWindSpeed(self, windSpeed):
        self.windSpeed = setWindSpeed

    def setWindDirection(self, windDirection):
        self.windDirection = windDirection
    
    def updateWindSpeed(self):
        if randrange(2) and self.windSpeed > 1:
            self.casuality = -self.casuality
        self.windSpeed = self.windSpeed+(randrange(10)*self.casuality)
    
    def updateWindDirection(self):
        if (randrange(10)/10) > self.changeDirectionThreshold:
            self.windDirection = self.directions[randrange(8)]
    
    def getSignature(self):
        item = {
            "name": self.name,
            "latitude": str(self.latitude),
            "longitude": str(self.longitude),
            "createdAt": int(self.createdAt)
        }
        return item
    
    def getMessage(self):
        message = {
            "name": self.name,
            "latitude": str(self.latitude),
            "longitude": str(self.longitude),
            "windSpeed": int(self.windSpeed),
            "windDirection": self.windDirection
        }
        return message
        
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