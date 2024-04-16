from django.urls import path
from confai.views import TickerView

urlpatterns = [
    path('ticker/<str:ticker>/', TickerView.as_view(), name='ticker'),
    path('ticker/<str:ticker>/<int:year>/<int:quarter>/', TickerView.as_view(), name='ticker_year_quarter'),
]