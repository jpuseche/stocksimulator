from django.db import models

class StockReport(models.Model):
    amount = models.IntegerField()
    quantity = models.IntegerField()
    transaction_cost = models.FloatField
    price = models.IntegerField()

    class Meta:
        managed: False
        app_label = 'stocksimulator'

class Csv (models.Model):
    csv_file = models.FileField(upload_to='stocksimulator/')
    class Meta:
        managed: False
        app_label = 'stocksimulator'
        
    def __str__(self):
        return f"file: {self.id}"