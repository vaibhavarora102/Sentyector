# Sentyector API

## Endpoints
- `api/audiochunktotext/`
  - Deployed: https://sentyectorapi.herokuapp.com/api/audiochunktotext/
  - Description: Speech to text
  - Method:`POST`
  - Working: Send a audio file in `.wav` format into `file` field and returns a identified text as output in JSON format
  
- `api/predemotions/`
  - Deployed: https://sentyectorapi.herokuapp.com/api/predemotions/
  - Description: Predicts emotions from text
  - Method:`POST`
  - Working: Send a text into `textopredict` field and returns a predicted Emotion as output in JSON format
  

Python code for calling API's
- `api/audiochunktotext/`
```
import requests
import json

url = 'https://sentyectorapi.herokuapp.com/api/audiochunktotext/'
files={'file':open(r'C:\Users\Sairish\Downloads\myrecord.wav','rb')}
r = requests.post(url, files = files)
print(r.text)
```
- `api/predemotions/`
```
import requests
import json

url = 'https://sentyectorapi.herokuapp.com/api/predemotions/'
data = {'textopredict': "You're just too good to be true can't take my eyes off you you'd be like heaven to touch I wanna hold you so much I love you baby"}
data = json.dumps(data)
r = requests.post(url, data = data)
print(r.text)
```