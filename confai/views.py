from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Prefetch, Q, F, Max

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from confai.models import ConferenceCall, Ticker
from confai.stanalysis.plotter import generate_stock_chart, plot_data
from confai.stanalysis.technical_analysis import StockAnalyzer

from confai.serializers import ConferenceCallSerializer

from datetime import timedelta

class TickerView(APIView):
    def get(self, request, ticker_symbol):
        ticker_obj = Ticker.objects.get(symbol=ticker_symbol)
        call = ConferenceCall.objects.filter(ticker=ticker_obj).latest('date')
        print(call)

        if call.average_scores and call.extreme_sentences and call.overall_sentiment:
            extreme_sentences = call.extreme_sentences
            formatted_extreme_sentences = {
                'negative': [(round(score, 2), sent) for score, sent in extreme_sentences[0]],
                'positive': [(round(score, 2), sent) for score, sent in extreme_sentences[1]],
            }

            result = {
                'sentiment_analysis': {
                    'weighted_average_sentiment': call.weighted_average_sentiment,
                    'extreme_sentences': formatted_extreme_sentences,
                    'overall_score': call.overall_sentiment,
                },
                'summary': call.summary,
                'full_text': call.full_text,
            }

            return Response({'call': result})

        return Response({'message': 'No call available for this ticker.'})

def ticker_list(request):
    sort = request.GET.get('sort', 'date')
    if sort == 'score':
        sort = 'max_weighted_average_sentiment'
    elif sort == 'date':
        sort = 'latest_date'
    today = timezone.now().date()
    seven_days_ago = today - timezone.timedelta(days=7)
    calls_in_last_seven_days = ConferenceCall.objects.filter(date__range=[seven_days_ago, today])
    calls_today = ConferenceCall.objects.filter(date=today)
    tickers_last_seven_days = Ticker.objects.filter(conferencecall__in=calls_in_last_seven_days).annotate(latest_date=Max('conferencecall__date'), max_weighted_average_sentiment=Max('conferencecall__weighted_average_sentiment')).order_by(sort)
    tickers_today = Ticker.objects.filter(conferencecall__in=calls_today).annotate(latest_date=Max('conferencecall__date'), max_weighted_average_sentiment=Max('conferencecall__weighted_average_sentiment')).order_by(sort)
    ticker_data_last_seven_days = [(ticker, ticker.conferencecall_set.order_by('-date')[0].weighted_average_sentiment if ticker.conferencecall_set.exists() else 'No call available') for ticker in tickers_last_seven_days]
    ticker_data_today = [(ticker, ticker.conferencecall_set.order_by('-date')[0].weighted_average_sentiment if ticker.conferencecall_set.exists() else 'No call available') for ticker in tickers_today]
    return render(request, 'ticker_list.html', {'ticker_data_today': ticker_data_today, 'ticker_data_last_seven_days': ticker_data_last_seven_days})

def all_calls(request):
    query = request.GET.get('q', '')
    all_calls = ConferenceCall.objects.filter(Q(ticker__symbol__icontains=query) | Q(summary__icontains=query)).order_by('-date')
    return render(request, 'all_calls.html', {'all_calls': all_calls})

def ticker_detail(request, ticker_symbol):
    ticker = get_object_or_404(Ticker, symbol=ticker_symbol)
    try:
        latest_call = ConferenceCall.objects.filter(ticker=ticker).latest('date')
    except ObjectDoesNotExist:
        return render(request, 'ticker_detail.html', {'ticker': ticker, 'message': 'No call available for this ticker.'})

    if latest_call.average_scores and latest_call.extreme_sentences and latest_call.overall_sentiment:
        extreme_sentences = latest_call.extreme_sentences
        formatted_extreme_sentences = {
            'negative': [(round(float(score), 2), sent) for score, sent in extreme_sentences['negative']],
            'positive': [(round(float(score), 2), sent) for score, sent in extreme_sentences['positive']],
        }

        result = {
            'sentiment_analysis': {
                'weighted_average_sentiment': latest_call.weighted_average_sentiment,
                'extreme_sentences': formatted_extreme_sentences,
                'overall_score': latest_call.overall_sentiment,
            },
            'summary': latest_call.summary,
            'full_text': latest_call.full_text,
        }

        return render(request, 'ticker_detail.html', {'ticker': ticker, 'latest_call': result})

    return render(request, 'ticker_detail.html', {'ticker': ticker, 'message': 'No call available for this ticker.'})
def call_detail(request, ticker_name, year, quarter):
    ticker = Ticker.objects.get(name=ticker_name)
    call = ConferenceCall.objects.get(ticker=ticker, year=year, quarter=quarter)
    return render(request, 'call_detail.html', {'call': call})

class LatestConferenceCallList(generics.ListAPIView):
    queryset = ConferenceCall.objects.order_by('-date')[:30]
    serializer_class = ConferenceCallSerializer