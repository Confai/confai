from rest_framework.views import APIView
from rest_framework.response import Response
from confai.models import Ticker, ConferenceCall
from django.shortcuts import render
from confai.five_indicators import StockAnalyzer
from confai.plotter import plot_data, generate_stock_chart
from django.shortcuts import get_object_or_404


class TickerView(APIView):
    def get(self, request, ticker, year=None, quarter=None):
        ticker_obj = Ticker.objects.get(name=ticker)
        calls = ConferenceCall.objects.filter(ticker=ticker_obj)

        if year and quarter:  # Filter by year and quarter if they are provided
            calls = calls.filter(year=year, quarter=quarter)

        results = []
        for call in calls:
            analyzer = sentiment.SentimentAnalyzer(call.full_text)
            avg_scores = analyzer.get_average_scores()
            extreme_sentences = analyzer.find_extreme_sentences()
            overall_score = analyzer.get_overall_score()

            summarizer = summary.DocumentSummarizer(call.full_text)
            summarized = summarizer.docsummarize()

            results.append({
                'sentiment_analysis': {
                    'average_scores': avg_scores.tolist(),  # Convert numpy array to list
                    'extreme_sentences': {
                        'negative': [sent for score, sent in extreme_sentences[0]],
                        'positive': [sent for score, sent in extreme_sentences[1]],
                    },
                    'overall_score': overall_score,
                },
                'summary': summarized,
            })

        return Response({'calls': results})

def ticker_list(request):
    tickers = Ticker.objects.all()
    return render(request, 'ticker_list.html', {'tickers': tickers})

def ticker_detail(request, ticker_name):
    ticker = get_object_or_404(Ticker, name=ticker_name)
    latest_call = ConferenceCall.objects.filter(ticker=ticker).latest('year', 'quarter')

    print(type(latest_call.average_scores))
    print(latest_call.extreme_sentences)

    analyzer = StockAnalyzer(ticker.name, '2007-01-01')  # Replace '2007-01-01' with the actual start date
    indicator_data = analyzer.get_all() # Get all the indicator data

    plots = plot_data(indicator_data)
    stock_chart = generate_stock_chart(ticker.name)  # Generate the stock chart

    return render(request, 'ticker_detail.html', {'ticker': ticker, 'latest_call': latest_call, 'plots': plots, 'stock_chart': stock_chart})

def call_detail(request, ticker_name, year, quarter):
    ticker = Ticker.objects.get(name=ticker_name)
    call = ConferenceCall.objects.get(ticker=ticker, year=year, quarter=quarter)
    return render(request, 'call_detail.html', {'call': call})