"""
@author: Harnick Khera (Github.com/Hephyrius)

Use this class as your pipeline, use it for all of your data manipulation/feature creation functionality.

Functions here are used across the bot and training classes!

"""
from binance.client import Client
import pandas as pd 
import numpy as np

#Get the balance of a specified coin
def getCoinBalance(client, currency):
    balance = float(client.get_asset_balance(asset=currency)['free'])
    return balance

#Market buy
def executeBuy(client, market, qtyBuy):
    
    order = client.order_market_buy(symbol=market,quantity=qtyBuy)

#Market sell
def executeSell(client, market, qtySell):

    order = client.order_market_sell(symbol=market, quantity=qtySell)

#format the data correctly for later use
def CreateOpenHighLowCloseVolumeData(indata):
    
    out = pd.DataFrame()
    
    d = []
    o = []
    h = []
    l = []
    c = []
    v = []
    for i in indata:
        #print(i)
        d.append(float(i[0]))
        o.append(float(i[1]))
        h.append(float(i[2]))
        c.append(float(i[3]))
        l.append(float(i[4]))
        v.append(float(i[5]))

    out['date'] = d
    out['open'] = o
    out['high'] = h
    out['low'] = l
    out['close'] = c
    out['volume'] = v
    
    #print(out)
    
    return out

#This is the main function for feature creation and manipulation, modify this by adding your own functions and feature creation
#prehaps try using technical analysis libraries for RSI or
#Sentiment data from bitfinex or Fear and greed data
def FeatureCreation(indata):
    
    convertedData = CreateOpenHighLowCloseVolumeData(indata)
    FeatureData = pd.DataFrame()
    FeatureData['o'] = convertedData['open']
    FeatureData['h'] = convertedData['high']
    FeatureData['l'] = convertedData['low']
    FeatureData['c'] = convertedData['close']
    FeatureData['v'] = convertedData['volume']
    candleRatios(FeatureData)
    StepData(FeatureData['c'],FeatureData)
    GetChangeData(FeatureData)
    
    return FeatureData
    
#Create targets for our machine learning model. This is done by predicting if the closing price of the next candle will 
#be higher or lower than the current one.
def CreateTargets(data, offset):
    
    y = []
    
    
    for i in range(0, len(data)-offset):
        current = float(data[i][3])
        comparison = float(data[i+offset][3])
        
        if current<comparison:
            y.append(1)

        elif current>=comparison:
            y.append(0)
            
    return y

#FEATURE EXAMPLES
#Calculate the change in the values of a column
def GetChangeData(x):

    cols = x.columns
    
    for i in cols:
        j = "c_" + i
        
        try:
            dif = x[i].diff()
            x[j] = dif
        except Exception as e:
            print(e)
            
#FEATURE EXAMPLES  
#Calculate the percentage change between this bar and the previoud x bars
def ChangeTime(x, step):
    
    out = []
    
    for i in range(len(x)):
        try:
            a = x[i]
            b = x[i-step]
            
            change = (1 - b/a) 
            out.append(change)
        except Exception as e:
            out.append(0)
    
    return out

#FEATURE EXAMPLES
#Automate the creation of percentage changes for 48 candles.  
def StepData(x, data):
    
    for i in range(1,48):
        
        data[str(i)+"StepDifference"] = ChangeTime(x, i)


#FEATURE EXAMPLES
#Features that take into acount the relations between the candle values  
def candleRatios(data):
    data['v_c'] = data['v'] / data['c']
    data['h_c'] = data['h'] / data['c']
    data['o_c'] = data['o'] / data['c']
    data['l_c'] = data['l'] / data['c']
    
    data['h_l'] = data['h'] / data['l']
    data['v_l'] = data['v'] / data['l']
    data['o_l'] = data['o'] / data['l']
    
    data['o_h'] = data['o'] / data['h']
    data['v_h'] = data['v'] / data['h']
    
    data['v_o'] = data['v'] / data['o']
