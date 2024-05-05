from rest_framework import serializers
from .models import ConferenceCall, Ticker
from confai.management.commands.dcf import DCF
import re

class ConferenceCallSerializer(serializers.ModelSerializer):
    percentile = serializers.FloatField(read_only=True)
    sentiment_category = serializers.CharField(read_only=True)
    full_text = serializers.SerializerMethodField()

    class Meta:
        model = ConferenceCall
        fields = ['year', 'quarter', 'summary', 'average_scores', 'extreme_sentences', 'overall_sentiment', 'weighted_average_sentiment', 'percentile', 'sentiment_category', 'full_text']

    def get_full_text(self, obj):
        return self.format_call_text(obj.full_text)

    def format_call_text(self, call_text):
        # The pattern matches any sequence of word characters, followed by optional spaces, another sequence of word characters, and a colon
        pattern = r"(\w+\s*\w*:)"
        # Add a newline before each match
        formatted_text = re.sub(pattern, r'\n\n\1', call_text)
        return formatted_text

class TickerSerializer(serializers.ModelSerializer):
    weighted_average_sentiment = serializers.FloatField(read_only=True)
    percentile = serializers.FloatField(read_only=True)
    sentiment_category = serializers.CharField(read_only=True)

    class Meta:
        model = Ticker
        fields = ['symbol', 'weighted_average_sentiment', 'percentile', 'sentiment_category']  # add other fields as needed


class SymbolSerializer(serializers.ModelSerializer):
    weighted_average_sentiment = serializers.FloatField(read_only=True)
    sentiment_category = serializers.CharField(read_only=True)
    news = serializers.SerializerMethodField()
    calls = serializers.SerializerMethodField()
    latest_call_info = serializers.SerializerMethodField()
    percentile = serializers.FloatField(read_only=True)
    class Meta:
        model = Ticker
        fields = ['symbol', 'weighted_average_sentiment', 'sentiment_category', 'percentile', 'news', 'calls', 'latest_call_info']

    def get_calls(self, obj):
        calls = ConferenceCall.objects.filter(ticker=obj).values('year', 'quarter')
        return list(calls)

    def get_news(self, obj):
        api = DCF()
        return api.get_news(obj.symbol)

    def get_latest_call_info(self, obj):
        latest_call = ConferenceCall.objects.filter(ticker=obj).latest('date')
        return {
            'year': latest_call.year,
            'quarter': latest_call.quarter,
            'date': latest_call.date,
            'weighted_average_sentiment': latest_call.weighted_average_sentiment,
            'summary': latest_call.summary,
            'full_text': self.format_call_text(latest_call.full_text),
            'negative_sentences': latest_call.extreme_sentences['negative'] if latest_call.extreme_sentences else None,
            'positive_sentences': latest_call.extreme_sentences['positive'] if latest_call.extreme_sentences else None
        }

    def format_call_text(self, call_text):
        # The pattern matches any sequence of word characters, followed by optional spaces, another sequence of word characters, and a colon
        pattern = r"(\w+\s*\w*:)"
        # Add a newline before each match
        formatted_text = re.sub(pattern, r'\n\n\1', call_text)
        return formatted_text