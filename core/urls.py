from django.urls import path
from confai import views

urlpatterns = [
    path('', views.ticker_list, name='ticker_list'),
    path('ticker/<str:ticker_name>/', views.ticker_detail, name='ticker_detail'),
    path('ticker/<str:ticker_name>/<int:year>/<int:quarter>/', views.call_detail, name='call_detail'),
]