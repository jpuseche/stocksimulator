from statistics import quantiles
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from . import actions

from stocksimulator.models import StockReport

def index(request):
    numberOfMonths = 2
    amountList = []
    quantityList = []
    priceList = []

    #get csv data here
    amountList.append(35328565993)
    amountList.append(14261061819)
    quantityList.append(9923633)
    quantityList.append(4047837)
    priceList.append(3598)
    priceList.append(3523)
    transaction_cost = 0.005

    portfolio = 0
    investment = []

    for i in range(numberOfMonths):
        boughtStocks, portfolio, investment = actions.buy(portfolio, amountList[i], investment, transaction_cost, quantityList[i]/2, priceList[i])
    for i in range(numberOfMonths):
        soldStocks, portfolio, investment = actions.sell(portfolio, amountList[i], investment, transaction_cost, quantityList[i]/2, priceList[i])
    netBoughtSoldValue = actions.netBoughtSoldValue(boughtStocks, soldStocks)
    predictedAmount = amountList[0] + netBoughtSoldValue

    boughtStocksCurrency = "${:,.2f}". format(boughtStocks)
    soldStocksCurrency = "${:,.2f}". format(soldStocks)
    netBoughtSoldValueCurrency = "${:,.2f}". format(netBoughtSoldValue)
    predictedAmountCurrency = "${:,.2f}". format(predictedAmount)


    companyName = "ecopetrol"
    return render(request, 'index.html', {
        "companyName": companyName,
        "boughtStocks": boughtStocksCurrency,
        "soldStocks": soldStocksCurrency,
        "netBoughtSoldValue": netBoughtSoldValueCurrency,
        "predictedAmount": predictedAmountCurrency,
        })