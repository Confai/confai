from django.urls import path
from confai import views
from django.contrib import admin
from confai.views import TickerListAPIView, CallDetailAPIView, SymbolAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ticker_list, name='ticker_list'),
    path('all_calls/', views.all_calls, name='all_calls'),
    path('ticker/<path:ticker_symbol>/', views.ticker_detail, name='ticker_detail'),
    path('api/symbol/<path:symbol>/', SymbolAPIView.as_view(), name='api_symbol_detail'),
    path('api/ticker_list/', TickerListAPIView.as_view(), name='api_ticker_list'),
    path('api/call_detail/<path:ticker_symbol>/<int:year>/<int:quarter>/', CallDetailAPIView.as_view(), name='api_call_detail'),
]