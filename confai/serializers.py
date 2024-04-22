from rest_framework import serializers
from .models import ConferenceCall

class ConferenceCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceCall
        fields = ['year', 'quarter', 'summary', 'average_scores', 'extreme_sentences', 'overall_sentiment', 'weighted_average_sentiment']