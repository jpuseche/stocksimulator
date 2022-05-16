from django.db import models

class StockReport(models.Model):
    amount = models.IntegerField()
    quantity = models.IntegerField()
    transaction_cost = models.FloatField
    price = models.IntegerField()

    class Meta:
        managed: False
        app_label = 'stocksimulator'