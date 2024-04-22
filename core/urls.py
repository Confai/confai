from django.urls import path
from confai import views

urlpatterns = [
    path('', views.ticker_list, name='ticker_list'),
    path('latest-calls/', views.LatestConferenceCallList.as_view(), name='latest-call-list'),
    path('ticker/<path:ticker_symbol>/', views.ticker_detail, name='ticker_detail'),
    path('ticker/<path:ticker_symbol>/<int:year>/<int:quarter>/', views.call_detail, name='call_detail'),
]