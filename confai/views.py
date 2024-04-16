from rest_framework.views import APIView
from rest_framework.response import Response
from confai.models import Ticker, ConferenceCall, TickerInfo


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