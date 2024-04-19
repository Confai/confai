from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView

from confai.models import ConferenceCall, Ticker
from confai.stanalysis.plotter import generate_stock_chart, plot_data
from confai.stanalysis.technical_analysis import StockAnalyzer

class TickerView(APIView):
    def get(self, request, ticker_symbol, year=None, quarter=None):
        ticker_obj = Ticker.objects.get(symbol=ticker_symbol)
        calls = ConferenceCall.objects.filter(ticker=ticker_obj)

        if year and quarter:  # Filter by year and quarter if they are provided
            calls = calls.filter(year=year, quarter=quarter)

        results = []
        for call in calls:
            print(call.extreme_sentences)
            print(call.overall_sentiment)
            print(call.weighted_average_sentiment)
            if call.average_scores and call.extreme_sentences and call.overall_sentiment:

                results.append({
                    'sentiment_analysis': {
                        'average_scores': call.average_scores,
                        'extreme_sentences': {
                            'negative': [sent for score, sent in extreme_sentences[0]],
                            'positive': [sent for score, sent in extreme_sentences[1]],
                        },
                        'overall_score': call.overall_sentiment,
                        'weighted_average_sentiment': call.weighted_average_sentiment,
                    },
                    'summary': call.summary,
                })

        return Response({'calls': results})

def ticker_list(request):
    tickers = Ticker.objects.all()
    return render(request, 'ticker_list.html', {'tickers': tickers})

def ticker_detail(request, ticker_symbol):
    ticker = get_object_or_404(Ticker, symbol=ticker_symbol)
    latest_call = ConferenceCall.objects.filter(ticker=ticker).latest('year', 'quarter')

    #analyzer = StockAnalyzer(ticker.name, '2024-01-01')  # Replace '2007-01-01' with the actual start date
    #indicator_data = analyzer.get_all() # Get all the indicator data

    #plots = plot_data(indicator_data)
    #stock_chart = generate_stock_chart(ticker.name)  # Generate the stock chart

    #return render(request, 'ticker_detail.html', {'ticker': ticker, 'latest_call': latest_call, 'plots': plots, 'stock_chart': stock_chart})

    return render(request, 'ticker_detail.html', {'ticker': ticker, 'latest_call': latest_call})
def call_detail(request, ticker_name, year, quarter):
    ticker = Ticker.objects.get(name=ticker_name)
    call = ConferenceCall.objects.get(ticker=ticker, year=year, quarter=quarter)
    return render(request, 'call_detail.html', {'call': call})