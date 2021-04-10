import requests
import json

# ---for prediciton---
url = 'http://127.0.0.1:8000/api/predemotions/'
data = {'textopredict': "You're just too good to be true can't take my eyes off you you'd be like heaven to touch I wanna hold you so much I love you baby"}
data = json.dumps(data)
r = requests.post(url, data = data)
print(r.text)

# ---for audiototext---
url = 'http://127.0.0.1:8000/api/audiochunktotext/'
files={'file':open(r'C:\Users\Sairish\Downloads\myrecord.wav','rb')}
r = requests.post(url, files = files)
print(r.text)