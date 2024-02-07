from django.db import models

# Create your models here.
class MarketSpread(models.Model):
    market = models.CharField(max_length=50, unique=True)
    spread = models.FloatField(default=0.0)
    alert_spread = models.FloatField(default=0.0)
    