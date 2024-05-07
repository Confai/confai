from django.contrib import admin
from confai.models import Ticker, ConferenceCall

# Register the Token model
admin.site.register(Ticker)
admin.site.register(ConferenceCall)