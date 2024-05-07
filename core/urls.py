from django.urls import path
from confai import views
from django.contrib import admin
from confai.views import TickerListAPIView, CallDetailAPIView, SymbolAPIView, AllCallsAPIView, PriorTickerListAPIView
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ticker_list, name='ticker_list'),
    path('all_calls/', views.all_calls, name='all_calls'),
    path('ticker/<path:ticker_symbol>/', views.ticker_detail, name='ticker_detail'),
    path('api/symbol/<path:symbol>/', SymbolAPIView.as_view(), name='api_symbol_detail'),
    path('api/ticker_list/', TickerListAPIView.as_view(), name='api_ticker_list'),
    path('api/call_detail/<path:ticker_symbol>/<int:year>/<int:quarter>/', CallDetailAPIView.as_view(), name='api_call_detail'),
    path('api/prior_ticker_list/', PriorTickerListAPIView.as_view(), name='api_prior_ticker_list'),
    path('api/all_calls/', AllCallsAPIView.as_view(), name='api_all_calls'),
    path('api-token-auth/', rest_views.obtain_auth_token, name='api_token_auth')
]