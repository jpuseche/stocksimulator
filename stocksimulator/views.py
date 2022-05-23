from statistics import quantiles
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from . import actions
import json 

from stocksimulator.models import StockReport

def home(request):
    monthsList = ["01/04/2022", "04/04/2022", "05/04/2022"]
    numberOfMonths = len(monthsList)
    amountList = []
    quantityList = []
    priceList = []

    #get csv data here
    amountList.append(35328565993)
    amountList.append(14261061819)
    amountList.append(23869850923)
    quantityList.append(9923633)
    quantityList.append(4047837)
    quantityList.append(6643194)
    priceList.append(3598)
    priceList.append(3523)
    priceList.append(3593)
    transaction_cost = 0.005

    portfolio = 0
    investment = []

    for i in range(numberOfMonths):
        boughtStocks, portfolio, investment = actions.buy(portfolio, amountList[i], investment, transaction_cost, quantityList[i]/2, priceList[i])
    for i in range(numberOfMonths):
        soldStocks, portfolio, investment = actions.sell(portfolio, amountList[i], investment, transaction_cost, quantityList[i]/2, priceList[i])
    netBoughtSoldValue = actions.netBoughtSoldValue(boughtStocks, soldStocks)
    predictedAmount = amountList[len(amountList)-1] + netBoughtSoldValue

    stocksBuyAndSell = [boughtStocks, soldStocks]

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
        "amountList": json.dumps(amountList),
        "monthsList": json.dumps(monthsList),
        "stocksBuyAndSell": json.dumps(stocksBuyAndSell),
        })

def import_csv(request):
    return render(request, 'import_csv.html', {

        })

def login(request):
    return render(request, 'login.html', {

        })        

def register(request):
    return render(request, 'register.html', {

        })

def forgot_password(request):
    return render(request, 'forgot-password.html', {

        })