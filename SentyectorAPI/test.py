import requests
import json

# ---for audiototext---
url = 'http://127.0.0.1:8000/api/audiochunktotext/'
# url = 'https://sentimentsapipractice.herokuapp.com/audiototext/'
files={'file':open(r'C:\Users\Sairish\Downloads\myrecord.wav','rb')}
r = requests.post(url, files = files)
print(r.text)