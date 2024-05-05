from django.urls import path
from confai import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ticker_list, name='ticker_list'),
    path('all_calls/', views.all_calls, name='all_calls'),
    path('latest-calls/', views.LatestConferenceCallList.as_view(), name='latest-call-list'),
    path('ticker/<path:ticker_symbol>/', views.ticker_detail, name='ticker_detail'),
    path('ticker/<path:ticker_symbol>/<int:year>/<int:quarter>/', views.call_detail, name='call_detail'),
]