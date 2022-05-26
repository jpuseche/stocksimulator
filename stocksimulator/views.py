from dataclasses import replace
from statistics import quantiles
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from . import actions
import json 
import csv
import string
from stocksimulator.models import StockReport
from .forms import CsvForm

daysList = []
amountList = []
quantityList = []
priceList = []
companyName=''
stocksBuyAndSell=[]
boughtStocksCurrency=''
boughtActions=[]

def home(request):
    
    # Se indica que las variables sean globales
    global companyName
    global daysList
    global amountList
    global quantityList
    global priceList
    global stocksBuyAndSell
    global boughtStocksCurrency
    global boughtActions
    #borra los daots de boughtActions
    boughtActions=[]
    #borra los datos de stocksBuyAndSell
    stocksBuyAndSell=[]
    #borra los datos de boughtStocksCurrency
    boughtStocksCurrency=''
    #borra los datos de companyName
    companyName=''
    #borra los datos de los arrays
    daysList=[]
    amountList=[]
    quantityList=[]
    priceList=[]
    print("boughtActions: ",boughtActions)
    #importa el csv
    #print("importando csv")
    form=request.GET
    #print(form)
    csv_file = form['CSVFile']
    #print(csv_file)
    with open(csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        cont=0
        for row in csv_reader:
            if cont!=0 :
              #print(row[3])
                companyName = row[0]
                #amountList
                volumen=int(row[3].replace('.', '').replace(',00', ''))
                amountList.append(volumen)
                #daysList
                fecha=row[1][:10]
                daysList.append(fecha)
                #quantityList
                Cantidad=int(row[2].replace('.', '').replace(',00', ''))
                quantityList.append(Cantidad)
                #priceList
                precio=row[6].replace('.', '')
                precio=precio.replace(',', '.')
                precio=float(precio)
                priceList.append(precio)
            cont=cont+1 
    
    transaction_cost = 0.005
    numberOfMonths=len(daysList)

    portfolio = 0
    investment = []
    #vacia boughtActions
    
    for i in range(numberOfMonths):
        boughtStocks, portfolio, investment  = actions.buy(portfolio, amountList[i], investment, transaction_cost, quantityList[i]/2, priceList[i])
        boughtActions.append(boughtStocks)

    #print("boughtStocks= ",boughtStocks," portfolio= ", portfolio ," investment= ", investment)
    for i in range(numberOfMonths):
        soldStocks, portfolio, investment = actions.sell(portfolio, amountList[i], investment, transaction_cost, quantityList[i]/2, priceList[i])
    netBoughtSoldValue = actions.netBoughtSoldValue(boughtStocks, soldStocks)
    predictedAmount = amountList[len(amountList)-1] + netBoughtSoldValue

    stocksBuyAndSell = [boughtStocks, soldStocks]

    boughtStocksCurrency = "${:,.2f}". format(boughtStocks)
    soldStocksCurrency = "${:,.2f}". format(soldStocks)
    netBoughtSoldValueCurrency = "${:,.2f}". format(netBoughtSoldValue)
    predictedAmountCurrency = "${:,.2f}". format(predictedAmount)
    
    
    
    return render(request, 'index.html', {
        "companyName": companyName,
        "boughtStocks": boughtStocksCurrency,
        "soldStocks": soldStocksCurrency,
        "netBoughtSoldValue": netBoughtSoldValueCurrency,
        "predictedAmount": predictedAmountCurrency,
        "amountList": json.dumps(amountList),
        "monthsList": json.dumps(daysList),
        "stocksBuyAndSell": json.dumps(stocksBuyAndSell),
        })

def reporte(request):
    AcionesVendidas=[]
    for i in range(len(boughtActions)):
        AcionesVendidas.append("${:,.2f}". format(boughtActions[i]))
    return render(request, 'reporte.html', {
        "companyName": companyName,
        "Transacciones": AcionesVendidas,
        "boughtStocks": boughtStocksCurrency,
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