"""
Program: urls.py
Author: Tom Sorteberg
Last date modified: 12/17/2020

The routing controller for the finalapp.
"""
from django.urls import path
from . import views

app_name = 'finalapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('bar_chart/', views.bar_chart, name='bar_chart'),
    path('pie_chart/', views.pie_chart, name='pie_chart'),
]
