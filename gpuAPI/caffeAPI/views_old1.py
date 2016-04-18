from django.shortcuts import render
from django.http import HttpResponse
import json
import sys
import urllib
import os
import random
import string


from threading import Thread
from time import sleep
from monitor import main as monitorProcess

if __name__ == "__main__":
    thread = Thread(target = monitorProcess, args = ("0.0.0.0",2))
    thread.start()
    print "thread finished...exiting"
	


global statusVal=0



from threading import Thread
from time import sleep

def threaded_function(arg):
    for i in range(arg):
        print "running"
        sleep(1)


thread = Thread(target = threaded_function, args = (10, ))
thread.start()
   # thread.join()
print "thread finished...exiting and still working"

def getStatus(request,*args, **kwargs):
    data=dict()

    modelName=request.GET.get('modelName','')
    imageURL=request.GET.get('imageURL','')
    data['imageURL']=imageURL
    if modelName=="":
        print "Using Default model"
    if imageURL=="":
        data['message']="empty field"
        data['result']=dict()
    else:
        data['message']="getting results"
        data['result']=computeTags(imageURL)

    return HttpResponse(json.dumps(data), content_type="application/json")  

