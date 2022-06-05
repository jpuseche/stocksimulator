from dataclasses import replace
from statistics import quantiles
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from numpy import size
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
boughtStocksCurrency=''
boughtActions=[]
soldActions=[]
boughtStocks=0
soldStocks=0
DiaDeCierre=''
CSVFILE='csv-files/ECOPETROL.csv'

def welcome(request):
        return render(request, 'welcome.html',{
        "csvFile": request.GET.get('CSVFile'),
    })


def home(request):
    
    # Se indica que las variables sean globales
    global companyName
    global daysList
    global amountList
    global quantityList
    global priceList
    global stocksBuyAndSell
    global boughtStocksCurrency
    global soldStocksCurrency
    global boughtActions
    global soldActions
    global boughtStocks
    global soldStocks
    global DiaDeCierre
    global CSVFILE
    #Borra el dato de dia de cierre
    DiaDeCierre=''
    #borra los daots de boughtActions
    boughtActions=[]
    #borra los datos de soldActions
    soldActions=[]
    #borra los datos de stocksBuyAndSell
    stocksBuyAndSell=[]
    #borra los datos de boughtStocksCurrency
    boughtStocksCurrency=''
    #borra los datos de soldStocksCurrency
    soldStocksCurrency=''
    #borra los datos de companyName
    companyName=''
    #borra los datos de los arrays
    daysList=[]
    amountList=[]
    quantityList=[]
    priceList=[]
    contNegatives=[]
    contPositives=[]
    #importa el csv
    #print("importando csv")
    #veifica si request.GET es valido

    form=request.GET
    try:
        csv_file = "csv-files/"+form['CSVFile']
        if (CSVFILE != 'csv-files/ECOPETROL.csv'):
            CSVFILE=''
            CSVFILE=csv_file
    except:
        print("no se pudo importar el csv")
        csv_file=CSVFILE
    
    with open(csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        cont=0
        contNegatives=0
        contPositives=0
        for row in csv_reader:
            if cont!=0 :
                companyName = row[0]
                #amountList
                if row[3]==",00":
                    amountList.append(0)
                else:
                    volumen=row[3].replace('.', '')
                    volumen=volumen.replace(',', '.')
                    volumen=float(volumen)
                    amountList.append(volumen)
                #daysList
                fecha=row[1][:10]
                daysList.append(fecha)
                #quantityList
                if row[2]==",00":
                    quantityList.append(0)
                else:
                    Cantidad=row[2].replace('.', '')
                    Cantidad=Cantidad.replace(',', '.')
                    Cantidad=float(Cantidad)
                    quantityList.append(Cantidad)
                #priceList
                if row[6]==",00":
                    priceList.append(0)
                else:
                    precio=row[6].replace('.', '')
                    precio=precio.replace(',', '.')
                    precio=float(precio)
                    priceList.append(precio)
                if row[9]!=",00":
                    variance=row[9].replace('.', '')
                    variance=variance.replace(',', '.')
                    if float(variance) <= 0:
                        contNegatives=contNegatives+1
                    else:
                        contPositives=contPositives+1
            cont=cont+1
    transaction_cost = 0.005
    numberOfMonths=len(daysList)

    portfolio = 0
    investment = []
    #vacia boughtActions
    
    for i in range(numberOfMonths):
        boughtStocks, portfolio, investment  = actions.buy(portfolio, amountList[i], investment, transaction_cost, quantityList[i]*((contPositives*100)/cont), priceList[i])
        boughtActions.append(boughtStocks)
    for i in range(numberOfMonths):
        soldStocks, portfolio, investment = actions.sell(portfolio, amountList[i], investment, transaction_cost, quantityList[i]*((contNegatives*100)/cont), priceList[i])
        soldActions.append(soldStocks)
    netBoughtSoldValue = actions.netBoughtSoldValue(boughtStocks, soldStocks)
    predictedAmount = amountList[len(amountList)-1] + netBoughtSoldValue

    moreSold = False
    if  (soldStocks > boughtStocks*-1):
        moreSold = True

    stocksBuyAndSell = [soldStocks, boughtStocks]

    boughtStocksCurrency = "${:,.2f}". format(boughtStocks)
    soldStocksCurrency = "${:,.2f}". format(soldStocks)
    netBoughtSoldValueCurrency = "${:,.2f}". format(netBoughtSoldValue)
    predictedAmountCurrency = "${:,.2f}". format(predictedAmount)
    
    DiaDeCierre=daysList[len(daysList)-1]
    
    return render(request, 'index.html', {
        "companyName": companyName,
        "boughtStocks": boughtStocksCurrency,
        "moreSold": moreSold,
        "soldStocks": soldStocksCurrency,
        "netBoughtSoldValue": netBoughtSoldValueCurrency,
        "predictedAmount": predictedAmountCurrency,
        "lineGraphic": json.dumps(amountList),
        "monthsList": json.dumps(daysList),
        "stocksBuyAndSell": json.dumps(stocksBuyAndSell),
        "csvFile": request.GET.get('CSVFile'),
        })

def stock_price(request):
    
    # Se indica que las variables sean globales
    global companyName
    global daysList
    global priceList
    global DiaDeCierre
    global CSVFILE
    #Borra el dato de dia de cierre
    DiaDeCierre=''
    #borra los daots de boughtActions
    boughtActions=[]
    #borra los datos de soldActions
    soldActions=[]
    #borra los datos de stocksBuyAndSell
    stocksBuyAndSell=[]
    #borra los datos de boughtStocksCurrency
    boughtStocksCurrency=''
    #borra los datos de soldStocksCurrency
    soldStocksCurrency=''
    #borra los datos de companyName
    companyName=''
    #borra los datos de los arrays
    daysList=[]

    #importa el csv
    #print("importando csv")
    #veifica si request.GET es valido

    form=request.GET
    try:
        csv_file = "csv-files/"+form['CSVFile']
        if (CSVFILE != 'csv-files/ECOPETROL.csv'):
            CSVFILE=''
            CSVFILE=csv_file
    except:
        print("no se pudo importar el csv")
        csv_file=CSVFILE
    
    with open(csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        cont=0
        contNegatives=0
        contPositives=0
        lastClosingPrice=0
        lastMajorPrice=0
        lastMediumPrice=0
        for row in csv_reader:
            if cont!=0 :
                companyName = row[0]
                #daysList
                fecha=row[1][:10]
                daysList.append(fecha)
                #priceList
                if row[6]==",00":
                    priceList.append(0)
                else:
                    mediumPrice=row[6].replace('.', '')
                    mediumPrice=mediumPrice.replace(',', '.')
                    mediumPrice=float(mediumPrice)
                    priceList.append(mediumPrice)
                #lastClosingPrice
                if row[4]!=",00":
                    closingPrice=row[4].replace('.', '')
                    closingPrice=closingPrice.replace(',', '.')
                    closingPrice=float(closingPrice)
                    lastClosingPrice="${:,.2f}". format(closingPrice)
                #lastMajorPrice
                if row[5]!=",00":
                    majorPrice=row[5].replace('.', '')
                    majorPrice=majorPrice.replace(',', '.')
                    majorPrice=float(majorPrice)
                    lastMajorPrice="${:,.2f}". format(majorPrice)
                #lastMajorPrice
                if row[6]!=",00":
                    lastMediumPrice="${:,.2f}". format(mediumPrice)
                #lastLowerPrice
                if row[7]!=",00":
                    lowerPrice=row[7].replace('.', '')
                    lowerPrice=lowerPrice.replace(',', '.')
                    lowerPrice=float(lowerPrice)
                    lastLowerPrice="${:,.2f}". format(lowerPrice)
                #variance
                if row[9]!=",00":
                    variance=row[9].replace('.', '')
                    variance=variance.replace(',', '.')
                    if float(variance) <= 0:
                        contNegatives=contNegatives+1
                    else:
                        contPositives=contPositives+1
            cont=cont+1

    moreSold = False
    if  (soldStocks > boughtStocks*-1):
        moreSold = True
    
    return render(request, 'stock_price.html', {
        "companyName": companyName,
        "lastClosingPrice": lastClosingPrice,
        "lastMajorPrice": lastMajorPrice,
        "lastMediumPrice": lastMediumPrice,
        "lastLowerPrice": lastLowerPrice,
        "lineGraphic": json.dumps(priceList),
        "moreSold": moreSold,
        "monthsList": json.dumps(daysList),
        "csvFile": request.GET.get('CSVFile'),
        })

def reporte(request):
    AcionesVendidas=[]
    pricesToShow=[]
    for i in range(len(boughtActions)):
        AcionesVendidas.append("${:,.2f}". format(boughtActions[i]))
        pricesToShow.append("${:,.2f}". format(priceList[i]))
    Descripcion="Estas fueron las acciones de la empresa "+companyName+" que fueron compradas al pasar del dia"
    stocksBuyAndSell = [boughtStocks, soldStocks]
    TipoDeTransaccion="Acciones Compradas"
    clase=False
    return render(request, 'reporte.html', {
        "companyName": companyName,
        "Transacciones": AcionesVendidas,
        "stocks": boughtStocksCurrency,
        "prices": pricesToShow,
        "description": Descripcion,
        "stocksBuyAndSell": json.dumps(stocksBuyAndSell),
        "TransactionType": TipoDeTransaccion,
        "Days":daysList,
        "ClosingDay":DiaDeCierre,
        "clase":clase,
        "csvFile": request.GET.get('CSVFile'),
        })
def soldReport(request):
    AcionesVendidas=[]
    pricesToShow=[]
    Descripcion="Estas fueron las acciones de la empresa "+companyName+" que fueron vendidas al pasar del dia"
    for i in range(len(soldActions)):
        AcionesVendidas.append("${:,.2f}". format(soldActions[i]))
        pricesToShow.append("${:,.2f}". format(priceList[i]))
    stocksBuyAndSell = [boughtStocks, soldStocks]
    TipoDeTransaccion="Acciones Vendidas"
    clase=True
    return render(request, 'reporte.html', {
        "companyName": companyName,
        "Transacciones": AcionesVendidas,
        "stocks": soldStocksCurrency,
        "prices": pricesToShow,
        "description": Descripcion,
        "stocksBuyAndSell": json.dumps(stocksBuyAndSell),
        "TransactionType": TipoDeTransaccion,
        "Days":daysList,
        "ClosingDay":DiaDeCierre,
        "clase":clase,
        "csvFile": request.GET.get('CSVFile'),
        })

def csv_files(request):
    return render(request, 'csv_files.html', {
        "csvFile": request.GET.get('CSVFile'),
        })

def learn_more(request):
    return render(request, 'learn_more.html',{
        "csvFile": request.GET.get('CSVFile'),
    })

def import_csv(request):

    return render(request, 'import_csv.html', {
        "csvFile": request.GET.get('CSVFile'),
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
def pro(request):
    return render(request, 'pro.html', {

        })