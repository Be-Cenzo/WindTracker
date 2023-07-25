import json
import sys

restid = sys.argv[1]
rest = {
    "rest_api_id": restid
}

webAppPath = "../web-app/src/app/rest.json"
sensorsPath = "../IoTSensors/rest.json"

webAppFile = open(webAppPath, "w") 
sensorsFile = open(sensorsPath, "w")

json.dump(rest, webAppFile, indent=2)
json.dump(rest, sensorsFile, indent=2)

webAppFile.close()
sensorsFile.close()