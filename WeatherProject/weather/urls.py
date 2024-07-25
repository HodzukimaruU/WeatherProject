from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('city_stats/', views.city_stats, name='city_stats'),
    path('repeat_search/<str:city>/', views.repeat_search, name='repeat_search'),
]
