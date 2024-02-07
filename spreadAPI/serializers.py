from rest_framework import serializers
from .models import MarketSpread

class MarketSpreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketSpread
        fields = '__all__' 

class UpdateMarketSpreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketSpread
        exclude = ['id', 'market', 'alert_spread']

class UpdateAlertSpread(serializers.ModelSerializer):
    class Meta:
        model = MarketSpread
        fields = ['alert_spread']
