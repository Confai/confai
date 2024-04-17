from rest_framework.views import APIView
from rest_framework.response import Response
from confai.models import Ticker, ConferenceCall
from django.shortcuts import render
from confai.five_indicators import StockAnalyzer
import matplotlib.pyplot as plt
import io
import base64

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
    ticker = Ticker.objects.get(name=ticker_name)

    analyzer = StockAnalyzer(ticker_name, '2007-01-01')  # Replace '2007-01-01' with the actual start date
    indicator_data = analyzer.get_all()

    # Generate plots for each dataset and convert them to base64
    plots = {}
    for key, data in indicator_data.items():
        fig, ax = plt.subplots()
        data.plot(ax=ax)
        plt.title(key)
        figfile = io.BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        figdata_png = base64.b64encode(figfile.getvalue()).decode('utf8')
        plots[key] = "data:image/png;base64," + figdata_png
        plt.close(fig)

    # Get the latest ConferenceCall for the selected Ticker
    latest_call = ConferenceCall.objects.filter(ticker=ticker).latest('year', 'quarter')

    return render(request, 'ticker_detail.html', {'ticker': ticker, 'plots': plots, 'latest_call': latest_call})

def call_detail(request, ticker_name, year, quarter):
    ticker = Ticker.objects.get(name=ticker_name)
    call = ConferenceCall.objects.get(ticker=ticker, year=year, quarter=quarter)
    return render(request, 'call_detail.html', {'call': call})