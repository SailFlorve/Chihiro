# -*-coding:utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from model.index_module import *
from model.search_engine import *


def hello(request):
    context = {}
    context['hello'] = 'Hello World!!!'
    return render(request, 'hello.html', context)


def welcome(request):
    context = {}
    #buildDB()
    return render(request, 'first-page.html', context)


def toFilmNameSearch(request):
    context = {}
    return render(request,'films-search.html', context)


def toDirectorNameSearch(request):
    context = {}
    return render(request,'director-search.html', context)


def toActorNameSearch(request):
    context = {}
    return render(request, 'actor-search.html', context)


@csrf_exempt
def test(request):
    soft_data = request.POST.get('softData')
    print("softData is ", soft_data)

    #jsonData 是一个字典（dict类型的变量）
    json_data = {
        'message': "test_data",
        'data': "杭电",
    }
    return JsonResponse(json.dumps(json_data), safe=False)


@csrf_exempt
def filmNameSearch(request):
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
        docs = get_doc(results)
        data = {
            'state': True,
            'data': docs
        }
        print(data)
        return JsonResponse(json.dumps(data), safe=False)


def get_doc(search_results):
    docs = list()
    for result in search_results:
        for doc in result[1]['docs']:
            docs.append(doc)
    return docs


def buildDB():
    db = IndexModule('statics/config.ini', 'utf-8')
    db.construct_postings_lists()




