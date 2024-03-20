from django.urls import path
from django.views.generic import RedirectView
from Dashboard import views

urlpatterns = [
    path('', RedirectView.as_view(url='home', permanent=False)),
    path('home', views.home, name='home'),
    path('odopProducts', views.odopProducts, name='odopProducts'),
    path('search', views.searchBox, name='searchBox'),
    path('dashboard', views.map_view, name='map_view'),
    path('crop-insights', views.CropInsights, name='CropInsights'),
]
