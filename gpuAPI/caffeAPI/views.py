from django.shortcuts import render
from django.http import HttpResponse
import json
import sys
sys.path.append('/home/ubuntu/caffe-cvprw15/examples/deepFashion/scripts')
import predictTags as predict
import getNear
import urllib
import os
import random
import string
import caffeClientManager as cCM

SETTINGS_FILE='/home/ubuntu/caffe-cvprw15/examples/deepFashion/label_jabong/SETTINGS.json'
numThreads=1
threadPoolObj=cCM.caffeThreadManager(numThreads,SETTINGS_FILE)


def compute(imageURL):
    filename=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))+'.jpg'
    filename='/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/'+filename
    if os.path.isfile(filename):
        os.remove(filename) 
    urllib.urlretrieve(imageURL, filename)
    classifier=threadPoolObj.getThread()
    if not classifier:
        print 'Unable to contact the weaver server'
        assert False
    print 'Recieved a Thread'
    embedding=predict.InputImagePredict(filename,SETTINGS_FILE,"embedding",classifier)
    
    threadPoolObj.returnThread(classifier)

    result=getNear.computeNN(SETTINGS_FILE, embedding)
    for i in range(len(result)):
        result[i]=result[i].strip()
        result[i]=result[i][8:]
        result[i]=result[i].replace("_", "/")
        result[i]=result[i].replace("catalog/s", "catalog_s")
    return result

def getNN(request,*args, **kwargs):
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
        data['result']=compute(imageURL)

    return HttpResponse(json.dumps(data), content_type="application/json")  


