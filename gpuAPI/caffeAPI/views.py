from django.shortcuts import render
# from rest_framework import status
from django.http import HttpResponse
import json
# Create your views here.

def getNN(request,*args, **kwargs):
    data=dict()
    print request
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
        data['result']={'res':'populate later'}

    return HttpResponse(json.dumps(data), content_type="application/json")  


