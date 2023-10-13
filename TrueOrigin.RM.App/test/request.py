import json
import requests

url = 'http://localhost/TrueOrigin.Portal/trueorigin.info/api/account/login'
myobj = {'email': 'trantrungbk95@gmail.com', "password": "1234567"}

x = requests.post(url, data = myobj)
if(x.status_code == 200):
    y = json.loads(x.text)
    access_token = (y["success"]['token'])
    print(format(access_token))

    url_info = 'http://localhost/TrueOrigin.Portal/trueorigin.info/api/account/info'

    result = requests.get(url_info,
        headers={'Content-Type':'application/json',
                'Authorization': 'Bearer {}'.format(access_token)})

    y = json.loads(x.text)
    print(result.text)

