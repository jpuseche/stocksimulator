from ast import For
from typing import ForwardRef
from django.contrib import admin

import csv

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def buy(portfolio, end_money, investment, transaction_cost, quantity, price):
    assigned_money = quantity*price
    end_money = end_money-assigned_money-transaction_cost*assigned_money
    portfolio += quantity
    if investment == []:
        investment.append(assigned_money)
    else:
        investment.append(assigned_money)
        investment[-1] += investment[-2]
    return end_money, portfolio, investment

#def totalBought(amount, transaction_cost, quantity, price):
    portfolio = 0
    investment = []
    end_money = amount
    end_money = buy(portfolio, end_money, investment, transaction_cost, quantity, price)
    boughtStocks = end_money
    return boughtStocks
        

def sell(portfolio, end_money, investment, transaction_cost, quantity, price):
    assigned_money = quantity*price
    end_money = end_money+assigned_money-transaction_cost*assigned_money
    portfolio -= quantity
    investment.append(-assigned_money)
    investment[-1] += investment[-2]
    return end_money, portfolio, investment

#def totalSold(amount, transaction_cost, quantity, price):
    portfolio = 0
    investment = []
    end_money = amount
    end_money = sell(portfolio, end_money, investment, transaction_cost, quantity, price)
    soldStocks = amount + end_money
    return soldStocks

def netBoughtSoldValue(totalBought, totalSold):
    netBoughtSoldValue = totalSold - totalBought
    print(totalBought)
    print(totalSold)
    return netBoughtSoldValue

def importCSV():
    with open('AccionDetalle.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
    
    return reader

def graphic(dates, mediumPrices):

    csvData = importCSV()

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    dates = [i for i in range(20)]
    mediumPrices = [np.sqrt(i**3) for i in date]

    def animate(i):
        global x,y
        r = np.random.normal(0,1,1)
        xar = x
        yar = y + r*y

        #ax1.clear()
        ax1.plot(xar,yar,marker='o')

    ani = animation.FuncAnimation(fig,animate,interval=1000)
    plt.show()

