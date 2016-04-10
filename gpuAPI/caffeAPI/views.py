from django.shortcuts import render
from django.http import HttpResponse
import json
import sys
sys.path.append('/home/ubuntu/caffe-cvprw15/examples/deepFashion/scripts')
import predict
import getNear
import urllib
import os

def compute(imageURL):
    if os.path.isfile('/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/0001.jpg'):
        os.remove('/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/0001.jpg') 
    urllib.urlretrieve(imageURL, '/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/0001.jpg')
    embedding=predict.InputImagePredict('/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/0001.jpg','/home/ubuntu/caffe-cvprw15/examples/deepFashion/label_jabong/SETTINGS.json')
    result=getNear.computeNN('/home/ubuntu/caffe-cvprw15/examples/deepFashion/label_jabong/SETTINGS.json', embedding)
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


