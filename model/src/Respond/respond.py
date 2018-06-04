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
    softData = request.POST.get('softData')
    print("softData is ", softData)

    #jsonData 是一个字典（dict类型的变量）
    jsonData = {
        'message': "testdata",
        'data': "杭电",
    }
    return JsonResponse(json.dumps(jsonData), safe=False)


@csrf_exempt
def filmNameSearch(request):
    film_name = request.GET.get('filmName')
    print("filmName is ", film_name)
    if not film_name:
        data = {
            'state': False,
            'message': "fail to recieve parameter"
        }
        print(data)
        return JsonResponse(json.dumps(data), safe=False)
    engine = SearchEngine('statics/config.ini', 'utf-8')
    flag, id_scores = engine.search(film_name)
    if flag == 0:
        data = {
            'state': False,
            'message': "No relevant data"
        }
        print(data)
        return JsonResponse(json.dumps(data), safe=False)
    else:
        doc_ids = [i for i, s in id_scores]
        docs = find(doc_ids)
        data = {
            'state': True,
            'data': docs
        }
        print(data)
        return JsonResponse(json.dumps(data), safe=False)


def find(docid):
    config = configparser.ConfigParser()
    config.read('statics/config.ini', 'utf-8')
    docs = []
    for id in docid:
        with open(config['DEFAULT']['doc_dir_path'] + id + '.json', 'r') as f:
            root = json.load(f)
            title = root['title']
            url = root['url']
            img = root['img']
            ename = root['ename']
            types = root['types']
            snippet = root['body'][0:120] + '……'
            directors = root['directors']
            actors = root['actors']
        doc = {'title': title, 'url': url, 'img': img, 'ename': ename, 'types': types, 'snippet': snippet,
               'directors': directors, 'actors': actors}
        docs.append(doc)
    return docs


def buildDB():
    db = IndexModule('statics/config.ini', 'utf-8')
    db.construct_postings_lists()




