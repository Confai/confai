from rest_framework.views import APIView
from rest_framework.response import Response
from confai.models import Ticker, ConferenceCall, TickerInfo
from django.shortcuts import render


class TickerView(APIView):
    def get(self, request, ticker, year=None, quarter=None):
        ticker_obj = Ticker.objects.get(name=ticker)  # Changed 'ticker' to 'name' as Ticker model has 'name' field
        ticker_info_objs = TickerInfo.objects.filter(ticker=ticker_obj)
        if year and quarter:  # Filter by year and quarter if they are provided
            ticker_info_objs = ticker_info_objs.filter(year=year, quarter=quarter)

        calls = ConferenceCall.objects.filter(ticker__in=ticker_info_objs)

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

        # Retrieve and return the TickerInfo instances associated with the requested ticker
        ticker_info = list(ticker_info_objs.values())  # Convert the QuerySet to a list of dictionaries

        return Response({'calls': results, 'ticker_info': ticker_info})
def ticker_list(request):
    tickers = Ticker.objects.all()
    return render(request, 'ticker_list.html', {'tickers': tickers})

def ticker_detail(request, ticker_name):
    ticker = Ticker.objects.get(name=ticker_name)
    ticker_info = TickerInfo.objects.filter(ticker=ticker)
    return render(request, 'ticker_detail.html', {'ticker': ticker, 'ticker_info': ticker_info})

def call_detail(request, ticker_name, year, quarter):
    ticker = Ticker.objects.get(name=ticker_name)
    ticker_info = TickerInfo.objects.get(ticker=ticker, year=year, quarter=quarter)
    call = ConferenceCall.objects.get(ticker=ticker_info)
    return render(request, 'call_detail.html', {'call': call})