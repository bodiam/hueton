import requests
import json

payload = json.dumps({"on":True})

r = requests.put("http://192.168.2.196/api/newdeveloper/lights/1/state", data = payload)

print r.status_code
