# -*-coding:utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from model.index_module import *
from model.search_engine import *

def welcome(request):
    context = {}
    #buildDB()
    return render(request, 'search.html', context)

def toSearch(request):
    context = {}
    #buildDB()
    return render(request, 'search.html', context)

@csrf_exempt
def test(request):
    soft_data = request.GET.get('softData')
    print("softData is ", soft_data)

    #jsonData 是一个字典（dict类型的变量）
    json_data = {
        'message': "test_data",
        'data': "杭电",
    }
    return JsonResponse(json.dumps(json_data), safe=False)


@csrf_exempt
def Search(request):
    film_name = request.GET.get('filmName')
    print("filmName is ", film_name)
    if not film_name:
        data = {
            'state': False,
            'message': "fail to receive parameter"
        }
        print(data)
        return JsonResponse(json.dumps(data), safe=False)
    engine = SearchEngine('statics/config.ini', 'utf-8')
    flag, results = engine.search(film_name)
    if flag == 0:
        data = {
            'state': False,
            'message': "No relevant data"
        }
        print(data)
        return JsonResponse(json.dumps(data), safe=False)
    else:
        print("to get_doc()")
        docs = get_doc(results)
        print("get docs")
        data = {
            'state': True,
            'data': docs
        }
        print(data)
        return JsonResponse(json.dumps(data), safe=False,content_type="application/json")


def get_doc(search_results):
    docs = list()
    for result in search_results:
        doc = result[1]['docs']
        #print("doc is ",doc)
        docs.append(doc)
    return docs


def buildDB():
    db = IndexModule('statics/config.ini', 'utf-8')
    db.construct_postings_lists()




