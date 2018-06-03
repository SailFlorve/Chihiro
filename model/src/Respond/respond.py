# -*-coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from model.search_engine import *
from model.index_module import *
import xml.etree.ElementTree as ET

def hello(request):
    context = {}
    context['hello'] = 'Hello World!!!'
    return render(request, 'hello.html', context)
def welcome(request):
    context = {}
    buildDB()
    return render(request, 'first-page.html', context)

def toFilmNameSearch(request):
    context = {}
    return render(request,'films-search.html',context)
def toDirectorNameSearch(request):
    context = {}
    return render(request,'director-search.html',context)
def toActorNameSearch(request):
    context = {}
    return render(request,'actor-search.html',context)


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


@csrf_exempt
def filmNameSearch(request):
    filmName = request.POST.get('filmName')
    print("filmName is ",filmName)
    engine = SearchEngine('statics/config.ini', 'utf-8')
    flag,id_scores = engine.search(filmName)
    if flag == 0:
        data = {
            'state':False,
            'message':"No relevant data"
        }
        print(data)
        return JsonResponse(json.dumps(data),safe=False)
    else:
        doc_ids = [i for i, s in id_scores]
        docs = find(doc_ids)
        data = {
            'state':True,
            'data':docs
        }
        print(data)
        return JsonResponse(json.dumps(data),safe=False)


def find(docid):
    docs = []
    dir_path = 'C:\\Users\\Administrator\\Desktop\\MassData\\Project\\Chihiro\\statics\\movies\\'
    for id in docid:
        root = ET.parse(dir_path + '%s.xml' % id).getroot()
        url = root.find('url').text
        title = root.find('title').text
        body = root.find('body').text
        img = root.find('img').text
        snippet = root.find('body').text[0:120] + '……'
        doc = {'url': url, 'title': title, 'snippet': snippet, 'body': body,
               'img': img, 'id': id}
        docs.append(doc)
    return docs

def buildDB():
    db = IndexModule('statics/config.ini', 'utf-8')
    db.construct_postings_lists()




