from datetime import datetime

from django.http import *
from django.shortcuts import *
from django.views.decorators.csrf import *

from firebase import firebase
firebase = firebase.FirebaseApplication('https://androidtemplate-f6fce-default-rtdb.firebaseio.com/', None)
result = firebase.get('/report/results/', '')
print(result)

def test(request):
    pic='elon-musk.jpg'
    x={'photo':pic}
    x=[]
    for i in result:
        p=str(datetime.fromtimestamp(float(i) / 1000.0))
        d={p:result[i]}
        x.append(d)
    print(x)
    return render(request,'index.html',{"ar":x})