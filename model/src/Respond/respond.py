# -*-coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

def hello(request):
    context = {}
    context['hello'] = 'Hello World!!!'
    return render(request, 'hello.html', context)
def welcome(request):
    context = {}
    return render(request, 'index.html', context)

@csrf_exempt
def test(request):
    softData = request.POST.get('softData')
    print("softData is ",softData)

    #jsonData 是一个字典（dict类型的变量）
    jsonData={
        'message':"testdata",
        'data':"杭电",
    }
    return JsonResponse(json.dumps(jsonData),safe=False)