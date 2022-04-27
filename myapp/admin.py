from django.contrib import admin

import csv

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import pandas as pd

amount = 1000
portfolio = 0
end_money = amount
investment = []
transaction_cost = 0.0075

def buy(quantity, price):
    global portfolio, end_money
    assigned_money = quantity*price
    end_money = end_money-assigned_money-transaction_cost*assigned_money
    portfolio += quantity
    if investment == []:
        investment.append(assigned_money)
    else:
        investment.append(assigned_money)
        investment[-1] += investment[-2]

def sell(quantity, price):
    global portfolio, end_money
    assigned_money = quantity*price
    end_money = end_money+assigned_money-transaction_cost*assigned_money
    portfolio -= quantity
    investment.append(-assigned_money)
    investment[-1] += investment[-2]

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

