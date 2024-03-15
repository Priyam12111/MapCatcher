from django.shortcuts import render
from django.urls import path
from Dashboard import views

urlpatterns = [
    path('', views.map_view, name='map_view'),
    path('crop-insights', views.CropInsights, name='CropInsights'),
]
