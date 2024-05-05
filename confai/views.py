from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Prefetch, Q, F, Max
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from confai.models import ConferenceCall, Ticker
from confai.management.commands.dcf import DCF
from confai.serializers import ConferenceCallSerializer
import re

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
    # Get the sort parameter from the request
    sort = request.GET.get('sort', 'date')
    if sort == 'score':
        sort = 'max_weighted_average_sentiment'
    elif sort == 'date':
        sort = 'latest_date'

    # Get today's date and yesterday's date
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    # Get the tickers for yesterday and today
    tickers_yesterday = Ticker.objects.filter(conferencecall__date=yesterday)
    tickers_today = Ticker.objects.filter(conferencecall__date=today)

    # Calculate the percentile for each ticker's weighted_average_sentiment
    for ticker in tickers_yesterday:
        latest_call = ConferenceCall.objects.filter(ticker=ticker).latest('date')
        queryset = ConferenceCall.objects.filter(ticker=ticker)
        percentile = calculate_percentile(queryset, latest_call.weighted_average_sentiment)
        ticker.percentile = percentile

    for ticker in tickers_today:
        latest_call = ConferenceCall.objects.filter(ticker=ticker).latest('date')
        queryset = ConferenceCall.objects.filter(ticker=ticker)
        percentile = calculate_percentile(queryset, latest_call.weighted_average_sentiment)
        ticker.percentile = percentile

    # Prepare the data for rendering
    ticker_data_yesterday = [(ticker, ticker.conferencecall_set.order_by('-date')[0].weighted_average_sentiment if ticker.conferencecall_set.exists() else 'No call available', 'positive' if ticker.percentile > 75 else 'neutral' if ticker.percentile > 25 else 'negative', ticker.percentile) for ticker in tickers_yesterday]
    ticker_data_today = [(ticker, ticker.conferencecall_set.order_by('-date')[0].weighted_average_sentiment if ticker.conferencecall_set.exists() else 'No call available', 'positive' if ticker.percentile > 75 else 'neutral' if ticker.percentile > 25 else 'negative', ticker.percentile) for ticker in tickers_today]

    # Render the template
    return render(request, 'ticker_list.html', {'ticker_data_yesterday': ticker_data_yesterday, 'ticker_data_today': ticker_data_today})

def all_calls(request):
    query = request.GET.get('q', '')
    all_calls = ConferenceCall.objects.filter(Q(ticker__symbol__icontains=query) | Q(summary__icontains=query)).order_by('-date')

    # Create a Paginator object
    paginator = Paginator(all_calls, 10)  # Show 10 calls per page

    # Get the page number from the request
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page_obj = paginator.get_page(page_number)

    # Pass the Page object to the template
    return render(request, 'all_calls.html', {'page_obj': page_obj})

def calculate_percentile(queryset, value):
    queryset = ConferenceCall.objects.all()
    count = queryset.count()
    if count == 0:
        return None

    below = queryset.filter(weighted_average_sentiment__lt=value).count()
    same = queryset.filter(weighted_average_sentiment=value).count()

    percentile = (100.0 * below + 50.0 * same) / count
    return percentile

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
            'full_text': format_call_text(latest_call.full_text),
        }


        # Calculate the percentile for the latest call's weighted_average_sentiment
        queryset = ConferenceCall.objects.filter(ticker=ticker)
        percentile = calculate_percentile(queryset, latest_call.weighted_average_sentiment)
        relative_score = 'positive' if percentile > 75 else 'neutral' if percentile > 25 else 'negative'

        api=DCF()
        news=api.get_news(ticker.symbol)

        return render(request, 'ticker_detail.html', {'ticker': ticker, 'latest_call': result, 'relative_score': relative_score, 'percentile': percentile, 'news': news})

    return render(request, 'ticker_detail.html', {'ticker': ticker, 'message': 'No call available for this ticker.'})
def call_detail(request, ticker_name, year, quarter):
    ticker = Ticker.objects.get(name=ticker_name)
    call = ConferenceCall.objects.get(ticker=ticker, year=year, quarter=quarter)
    return render(request, 'call_detail.html', {'call': call})

class LatestConferenceCallList(generics.ListAPIView):
    queryset = ConferenceCall.objects.order_by('-date')[:30]
    serializer_class = ConferenceCallSerializer

def format_call_text(call_text):
    # The pattern matches any sequence of word characters, followed by optional spaces, another sequence of word characters, and a colon
    pattern = r"(\w+\s*\w*:)"
    # Add a newline before each match
    formatted_text = re.sub(pattern, r'\n\n\1', call_text)
    return formatted_text