from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Count, Prefetch, Q, F, Max
from django.core.paginator import Paginator
from django.views.generic import ListView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination, CursorPagination
from confai.models import ConferenceCall, Ticker
from confai.management.commands.dcf import DCF
from confai.serializers import ConferenceCallSerializer, TickerSerializer, SymbolSerializer, AllCallsSerializer

################### Temporary Template Views ###################
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
        ticker.percentile, ticker.category = ConferenceCall.percentile(latest_call)

    for ticker in tickers_today:
        latest_call = ConferenceCall.objects.filter(ticker=ticker).latest('date')
        ticker.percentile, ticker.category = ConferenceCall.percentile(latest_call)


    # Prepare the data for rendering
    ticker_data_yesterday = [(ticker, ticker.conferencecall_set.order_by('-date')[0].weighted_average_sentiment if ticker.conferencecall_set.exists() else 'No call available', ticker.category, ticker.percentile) for ticker in tickers_yesterday]
    ticker_data_today = [(ticker, ticker.conferencecall_set.order_by('-date')[0].weighted_average_sentiment if ticker.conferencecall_set.exists() else 'No call available', ticker.category, ticker.percentile) for ticker in tickers_today]

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
            'full_text': ConferenceCall.format_call_text(latest_call.full_text)
        }


        # Calculate the percentile for the latest call's weighted_average_sentiment
        queryset = ConferenceCall.objects.filter(ticker=ticker)
        percentile, relative_score = ConferenceCall.percentile(latest_call)

        api=DCF()
        news=api.get_news(ticker.symbol)

        return render(request, 'ticker_detail.html', {'ticker': ticker, 'latest_call': result, 'relative_score': relative_score, 'percentile': percentile, 'news': news})

    return render(request, 'ticker_detail.html', {'ticker': ticker, 'message': 'No call available for this ticker.'})

################### API Views ###################

class TickerListAPIView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        today = datetime.now().date()
        tickers_today = Ticker.objects.filter(conferencecall__date=today)

        # Prepare the data for rendering
        ticker_data_today = [{'symbol': ticker.symbol,
                              'weighted_average_sentiment': ticker.conferencecall_set.order_by('-date')[0].weighted_average_sentiment if ticker.conferencecall_set.exists() else None,
                              'sentiment_category': ConferenceCall.percentile(ticker.conferencecall_set.order_by('-date')[0])[1] if ticker.conferencecall_set.exists() else None,
                              'percentile': ConferenceCall.percentile(ticker.conferencecall_set.order_by('-date')[0])[0] if ticker.conferencecall_set.exists() else None}
                             for ticker in tickers_today]

        # Serialize the data
        serializer_today = TickerSerializer(ticker_data_today, many=True)

        # Return the serialized data
        return Response({'ticker_data_today': serializer_today.data})

class CustomCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-latest_call_date'

class PriorTickerListAPIView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        count = request.GET.get('count', 10)  # Get the count parameter from the request, default to 10 if not provided
        count = int(count)  # Convert the count to an integer

        today = datetime.now().date()

        # Annotate each ticker with the date of the latest call and filter in a single query
        tickers_before_today = Ticker.objects.filter(conferencecall__date__lt=today).annotate(latest_call_date=Max('conferencecall__date'))

        # Create a paginator
        paginator = CustomCursorPagination()
        paginator.page_size = count

        # Apply pagination to the queryset
        paginated_tickers = paginator.paginate_queryset(tickers_before_today, request)

        # Prepare the data for rendering
        ticker_data_before_today = [{'symbol': ticker.symbol,
                                     'weighted_average_sentiment': ticker.conferencecall_set.order_by('-date')[0].weighted_average_sentiment if ticker.conferencecall_set.exists() else None,
                                     'sentiment_category': ConferenceCall.percentile(ticker.conferencecall_set.order_by('-date')[0])[1] if ticker.conferencecall_set.exists() else None,
                                     'percentile': ConferenceCall.percentile(ticker.conferencecall_set.order_by('-date')[0])[0] if ticker.conferencecall_set.exists() else None}
                                    for ticker in paginated_tickers]

        # Serialize the data
        serializer_before_today = TickerSerializer(ticker_data_before_today, many=True)

        # Return the paginated response
        return paginator.get_paginated_response(serializer_before_today.data)

class CallDetailAPIView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def get(self, request, ticker_symbol, year, quarter, format=None):
        # Use select_related to retrieve the Ticker and ConferenceCall objects in a single query
        call = get_object_or_404(ConferenceCall.objects.select_related('ticker'), ticker__symbol=ticker_symbol, year=year, quarter=quarter)

        # Calculate the percentile for the call's weighted_average_sentiment
        percentile, category = ConferenceCall.percentile(call)
        call.percentile = percentile
        call.sentiment_category = category

        # Serialize the data
        serializer = ConferenceCallSerializer(call)

        # Return the serialized data
        return Response(serializer.data)

class SymbolAPIView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def get(self, request, symbol, format=None):
        ticker = get_object_or_404(Ticker, symbol=symbol)
        latest_call = ConferenceCall.objects.filter(ticker=ticker).latest('date')

        percentile, category = ConferenceCall.percentile(latest_call)

        ticker.percentile = percentile
        ticker.sentiment_category = category

        # Serialize the data
        serializer = SymbolSerializer(ticker)

        # Return the serialized data
        return Response(serializer.data)

class AllCallsAPIView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        query = request.GET.get('q', '')
        sort = request.GET.get('sort', 'date')

        sort_options = {
            'date': 'date',
            'score': 'weighted_average_sentiment',
            'name': 'ticker__symbol'
        }

        all_calls = ConferenceCall.objects.filter(Q(ticker__symbol__icontains=query) | Q(summary__icontains=query)).order_by('-date')

        # Check if the provided sort option exists, if not, default to 'date'
        sort_field = sort_options.get(sort, 'date')

        # Create a Paginator object
        paginator = Paginator(all_calls, 10)  # Show 10 calls per page

        # Get the page number from the request
        page_number = request.GET.get('page')

        # Get the Page object for the current page
        page_obj = paginator.get_page(page_number)

        # Serialize the data
        serializer = AllCallsSerializer(page_obj, many=True)

        # Return the serialized data
        return Response(serializer.data)