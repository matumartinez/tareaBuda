from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from . models import MarketSpread
from . serializers import UpdateMarketSpreadSerializer
from requests import get
import json

# Create your tests here.
class Setup(TestCase):
    def setUp(self):
        markets = get('https://www.buda.com/api/v2/markets').json()['markets']
        for market in markets:
            market_id = market['id'].lower()
            ticker = get(f'https://www.buda.com/api/v2/markets/{market_id}/ticker').json()['ticker']
            spread = round(float(ticker['min_ask'][0]) - float(ticker['max_bid'][0]), 2)
            spread_object, created = MarketSpread.objects.get_or_create(
                market = market_id,
                defaults = {
                    'spread': spread
                }
            )
            data = {'spread': spread}
            serializer = UpdateMarketSpreadSerializer(spread_object, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()

class MarketSpreadTests(Setup):
    client = APIClient()

    def setUp(self):
        super().setUp()
    
    def test_get_spreads(self):
        response = self.client.get('/spreads/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])
        print("TEST GET SPREADS PASSED")
        print(' ')
    
    def test_get_single_spread(self):
        response = self.client.get('/spreads/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])
        print("TEST GET SINGLE SPREAD PASSED")
        print(' ')
    
    def test_patch_alert_spread(self):
        data = json.dumps({'alert_spread': 0.0})
        response = self.client.patch('/spreads/1', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.dumps({'alert_spread': "hello"})
        response = self.client.patch('/spreads/1', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("TEST UPDATE ALERT SPREAD PASSED")
        print(' ')
