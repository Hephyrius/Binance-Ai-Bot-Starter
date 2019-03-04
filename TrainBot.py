# -*- coding: utf-8 -*-
"""
@author: Harnick Khera (Github.com/Hephyrius)

Use this class to train a basic machine learning model. Or modify it to incoportate your own machine learning models or Pipelines by
using other libraries such as XGBoost, Keras or strategies like Spiking Neural Networks!

"""

import numpy as np
from numpy import *
import pandas as pd

from binance.client import Client
from binance.enums import *


import CoreFunctions as cf

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, mean_squared_error
from joblib import dump, load

#You don't need to enter your key/secret in order to get data from the exchange, its only needed for trades in the TradingBot.py class.
api_key = '0'
api_secret = '0'
client = Client(api_key, api_secret)

candles = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "01 Jan, 2017", "10 Jul, 2020")

#Convert the raw data from the exchange into a friendlier form with some basic feature creation
convertedData = cf.CreateOpenHighLowCloseVolumeData(candles)
sm = pd.DataFrame()
sm['o'] = convertedData['open']
sm['h'] = convertedData['high']
sm['l'] = convertedData['low']
sm['c'] = convertedData['close']
sm['v'] = convertedData['volume']

offset = 0
y = cf.CreateTargets(candles,1)
y = y[94:]

cf.StepData(sm['c'],sm)
cf.GetChangeData(sm)
x = sm[94:len(candles)-1]

#produce sets, avoiding overlaps!
#data is seporated temporily rather than randomly
#this prevents the model learning stuff it wouldnt know - aka leakage - which can give us false positive models
trny = y[:9999]
trnx = x[:9999]

#Validation set is not used in this starter model, but should be used if using other libraries that support early stopping.
valy = y[10000:12999]
valx = x[10000:12999]

tsty = y[13000:]
tstx = x[13000:]

model = GradientBoostingClassifier() 
model.fit(trnx,trny)

preds = model.predict(tstx)

#Some basic tests so we know how well our model performs on unseen - "modern" data.
#Helps with fine tuning features and model parameters
accuracy = accuracy_score(tsty, preds)
mse = mean_squared_error(tsty, preds)

print("Accuracy = " + str(accuracy))
print("MSE = " + str(mse))

falsePos = 0
falseNeg = 0
truePos = 0
trueNeg = 0
total = len(preds)

for i in range(len(preds)):
    
    if preds[i] == tsty[i] and tsty[i] == 1:
        truePos +=1
        
    elif preds[i] == tsty[i] and tsty[i] == 0:
        trueNeg +=1
        
    elif preds[i] != tsty[i] and tsty[i] == 1:
        falsePos +=1
        
    elif preds[i] != tsty[i] and tsty[i] == 0:
        falseNeg +=1
        
print("False Pos = " + str(falsePos/total))
print("False Neg = " + str(falseNeg/total))
print("True Pos = " + str(truePos/total))
print("True Neg = " + str(trueNeg/total))

#how important of the features - helps with feature selection and creation!
results = pd.DataFrame()
results['names'] = trnx.columns
results['importance'] = model.feature_importances_
print(results.head)


#save our model to the system for use in the bot
dump(model, open("Models/model.mdl", 'wb'))








