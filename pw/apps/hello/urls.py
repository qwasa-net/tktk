# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

urlpatterns = [
    # profile page
    url(r'^there', views.there, name='hello-there'),
    # logout
    url(r'^(logout|bye)/*[0-9]*', views.bye, name='hello-bye'),
    # login or log in
    url(r'.*', views.iam, name='hello-iam')
]
