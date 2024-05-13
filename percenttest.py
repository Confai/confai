from django.db.models import F, Window
from django.db.models.functions import PercentRank
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from confai.models import ConferenceCall

results = ConferenceCall.objects.annotate(
    percentile=Window(
        expression=PercentRank(),
        order_by=F('weighted_average_sentiment').asc()
    ) * 100
)

for result in results:
    print(result.weighted_average_sentiment, result.percentile)