import requests
import json
import time

url = "http://192.168.100.14:2000/get_employee2"
expired_date = time.time() + 60
body = { "username": "vinhnl"}
# encoded_jwt = jwt.encode(body, client_secret, algorithm="HS256")
payload = json.dumps(body)
headers = { 'Content-Type': 'application/json' }

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)