# Binance-Ai-Bot-Starter
Boilerplate/Starter code for trading on [Binance Exchange](https://www.binance.com/?ref=25062167) using Machine Learning. The provided code uses a bare bones gradient boosting model that can trade on live markets, using hourly candle data.

## Disclaimer:

### This bot is intended to be a Proof-of-concept/Starter-kit. The developer will not be responsible for Any losses that are made are as a result of using this tool. Understand the risks involved and Only invest amounts you are willing to lose.  

## Supporting:

If you appreciate my work send all crypto donations in Eth, Bnb, Matic, Avax etc on any chain to : 0xe0a09b49721FBD8B23c67a3a9fdE44be4412B8fD

## What is this?

This repository is a quickstart/boilerplate for getting machine learning based trading bots up and running. It provides a basic pipeline for training and deploying models, as well as creating some example features that could be used in a model.

## Requirements:
[Binance Account](https://www.binance.com/?ref=25062167)

### Required Python 3 Libraries:

Python-Binance

Sklearn

Pandas

Numpy

Joblib

## Usage:
Replace the values in api_key and api_secret in the TradingBot.py file with your own keys generated via the Binance account console. Once this is done, simply run the TradingBot.py file to run the provided model or your own trained models. To end the program, simple stop the python console.

## Customisation:

The core of the code is the CoreFunctions class. It is recommended that you modify this with your own feature creation. An example would be to create functions for calculating the values of RSI and MACD indicators, or calculating moving avarages. You should add all new features as an additional column to the dataframe. I recommend making changes to the "FeatureCreation" function in "CoreFunctions.py" as this is where the manipulation takes place.

Using different machine learning models is fairly simple. Just substitute all references to "model" to that of your own machine learning model. Most libraries can handle the data as formatted by this code, without any changes.

## Q and A:

### Does this make money?

Well, this depends on you and your machine learning strategies! You could come up with some very powerful models that beat the market, or you could come up with models that are patchy. I recomend you do a lot of testing before using the bot on live markets, or you might get crushed!

### Do I use this?

I don't use this exact code. Infact this codebase is derived from my own bot that I do use. I have my own feature creation and other methods for my models with a suprisingly high accuracy (~84% on BTCUSDT). Deciding on machine learning model and features is core to a good bot.
