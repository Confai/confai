from rest_framework import serializers
from .models import ConferenceCall, Ticker

class ConferenceCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceCall
        fields = ['year', 'quarter', 'summary', 'average_scores', 'extreme_sentences', 'overall_sentiment', 'weighted_average_sentiment']

class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = ['symbol', 'name']  # add more fields if needed