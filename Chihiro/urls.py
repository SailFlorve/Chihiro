"""Chihiro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url

from model.src.Respond import respond

urlpatterns = [
    url(r'^hello$', respond.hello),
    url(r'^$', respond.welcome),
    url(r'^test$', respond.test),
    url(r'^fieldNameDownloadable.do/Disease$', respond.toFilmNameSearch),
    url(r'^fieldNameDownloadable.do/Weather$', respond.toDirectorNameSearch),
    url(r'^fieldNameDownloadable.do/Station$', respond.toActorNameSearch),
    url(r'^filmNameSearch$', respond.filmNameSearch)
]
