# -*- coding: utf-8 -*-
"""
@author: Harnick Khera (Github.com/Hephyrius)

Use this class to trade using the model trained using the TrainBot class. This model is loaded from the "Models" folder.
"""
from numpy import *
import numpy as np
import pandas as pd
import time

from binance.client import Client
from binance.enums import *

import datetime
import CoreFunctions as cf
from joblib import dump, load

#%%

api_key = 'INSERT YOUR KEY'
api_secret = 'INSERT YOUR SECRET'

client = Client(api_key, api_secret)

model = load("Models/model.mdl")

firstRun = True
makeTrade = False

state = 0
prevTime = 0

data = []
MLData = []

currentBtc = cf.getCoinBalance(client, 'btc')
print(currentBtc)
currentUSDT = cf.getCoinBalance(client, 'USDT')
print(currentUSDT)

hasToken = False
currentTokenBalance = 0

market = "BTCUSDT"
trade = "BTC"
sellToBuyTransition = True

buyPrice = 0
bestPrice = 0
sinceBest = 0

while(True):
    
    #check time stamp if its different then add to list and change state
    if state == 0:
        
        candles = client.get_klines(symbol=market, interval=Client.KLINE_INTERVAL_1HOUR)
        
        if firstRun == True:
            prevTime = datetime.datetime.fromtimestamp(candles[498][0]/ 1e3)
            
            firstRun = False
            makeTrade = False
            for i in range(499):
                data.append(candles[i])
            
        else:
            currTime = datetime.datetime.fromtimestamp(candles[498][0]/ 1e3)
            
            if prevTime != currTime:
                if candles[498] not in data:
                    data.append(candles[498])
                    prevTime = currTime
                    makeTrade = True
                
            else:
                
                makeTrade = False
                
        print(makeTrade)
        state = 1
        
    #Trailing Stoploss at 1% of highest price since entering trade. Checking highest value every 10 seconds, helps prevent against BIG dumps or bad predictions 
    #in the hour
    if state == 1:

        if hasToken == True:
            try:
                
                prices =  client.get_order_book(symbol=market)
                price = prices['bids'][0][0]
                
                if float(price) > float(bestPrice):
                    
                    bestPrice = price
                    
                elif bestPrice * 0.99 > price:
                    
                    print("Selling")                    
                    
                    sellAmt = cf.getCoinBalance(client, trade)
                    currentBtc = str(sellAmt)
                    qty = ""
                    
                    for q in range(8):
                        qty += currentBtc[q]
                    
                    currentBtc = qty
                    
                    cf.executeSell(client, market, currentBtc)
                    currentTokenBalance = 0
                    hasToken = False
                    sellToBuyTransition = False
                    buyPrice = 0
                    bestPrice = 0
                    sinceBest = 0
                    currentBtc = cf.getCoinBalance(client, 'btc')
                    print("Trailing Stop Trigger")        
                    state = 0
                    time.sleep(10)
                                    
            except Exception as e:
                print(e)
        
        # if timestamp is different then we update the 
        if makeTrade == True:
            state = 2
            makeTrade = False
        else:
            state = 0
            time.sleep(10)
            
    #make feature data used to make prediction
    if state == 2:
        #data = cf.makeTrainingData(data)
        convertedData = cf.CreateOpenHighLowCloseVolumeData(data)
        MLData = pd.DataFrame()
        MLData['o'] = convertedData['open']
        MLData['h'] = convertedData['high']
        MLData['l'] = convertedData['low']
        MLData['c'] = convertedData['close']
        MLData['v'] = convertedData['volume']
        cf.StepData(MLData['c'],MLData)
        cf.GetChangeData(MLData)
        print(1)
        state = 3
    
    #make trade based on predicted signal
    if state == 3:
        
        pred = model.predict_proba(MLData[len(MLData)-1:len(MLData)])
        print(pred[0])
        signal = np.argmax(pred[0])
        print(signal)
        
        #If the model buys then market buy as long as we do not currently have BTC and as long as we are going from a Sell signal previously, 
        #to a buy signal now
        if signal == 1:
            print("Buy Signal")
            
            if hasToken == False and sellToBuyTransition == True:
                try:
                    print("Buying")
                    currentUSDT = cf.getCoinBalance(client, 'USDT')
                    
                    prices =  client.get_order_book(symbol=market)
                    price = prices['asks'][0][0]
                    buyPrice = price
                    bestPrice = buyPrice
                    buyAmt =  currentUSDT/float(price)
                    buyAmt = str(buyAmt)
                    qty = ""
                    for q in range(8):
                        qty += buyAmt[q]
                    
                    buyAmt = qty
                    cf.executeBuy(client, market, buyAmt)
                    currentTokenBalance = buyAmt
                    hasToken = True
                    
                    state = 0
                    time.sleep(10)
                    
                except Exception as e:
                    print(e)
            else:
                state = 0
                time.sleep(10)
        
        #Only sells when we actually have BTC to market sell!
        if signal == 0:
            print("Sell Signal")
            
            if sellToBuyTransition == False:
                sellToBuyTransition = True
                
            if hasToken == True:
                try:
                    print("Selling")                    
                    currentBtc = cf.getCoinBalance(client, 'BTC') 
                    
                    currentBtc = str(currentBtc)
                    qty = ""
                    
                    for q in range(8):
                        qty += currentBtc[q]
                    
                    currentBtc = qty
                    cf.executeSell(client, market, currentBtc)
                    currentTokenBalance = 0
                    hasToken = False
                    
                    state = 0
                    time.sleep(10)
                    
                except Exception as e:
                    print(e)
            else:
                state = 0
                time.sleep(10)
                
