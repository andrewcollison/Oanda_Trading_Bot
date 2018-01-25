import pandas as pd
import numpy as np
import requests
import json
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt
style.use('ggplot')

class collect_data: # aquire historic data from Oanda api
	def get_data(instrument):
		url = "https://api-fxtrade.oanda.com/v1/candles?instrument={}&count=5000&candleFormat=midpoint&granularity=D&dailyAlignment=0&alignmentTimezone=America%2FNew_York".format(instrument) 
		resp = requests.get(url)
		data = json.loads(resp.text)
		data = pd.DataFrame(data['candles'])

		data['time'] = pd.to_datetime(data['time'])
		# data = data.set_index('time')
		# data['time'] = dt.datetime.strptime(str(data['time']), '%Y-%m-%d %H:%M:%S')
		# data['time'] = data['time'].date()
		data = data.rename(index=str, columns={"closeMid": "Close", "highMid": "High", "lowMid": "Low", "openMid":"Open"})
		data = data.drop('complete', 1)
		return data

class indicators: # Calculate Relevant Indicator Values 		
	
	def Moving_Average(data):
		MA = data['Close'].rolling(center=False, window=20).mean()
		MA_20d = pd.DataFrame({'MA_20d': MA})
		# print(MA_20d)
		return MA_20d

	def ExpMovingAverage(data):
		ewm = data.Close.ewm(span=20, adjust=True, min_periods=20).mean()
		return pd.DataFrame({"ewm":ewm})

	def AverageTrueRange(data):
		H_minus_L = data.High - data.Low
		H_minus_Cp = data.High - data.Close
		L_minus_Cp = data.Low - data.Close

		ATR_calc = pd.DataFrame({'H-L': H_minus_L, 'H-CP': H_minus_Cp, 'L-CP': L_minus_Cp})

		ATR = ATR_calc.max(axis=1)
		ATR = ATR.ewm(span=20, adjust=True, min_periods=20).mean() # exponential moving average

		ATR = pd.DataFrame({'ATR': ATR})
		return ATR 

	def keltner_channel(data):
		ATR = None
		ExpMa = None
		kelt_upper = ExpMa + (1*ATR)
		kelt_lower = ExpMa - (1*ATR)

		kelt_data = pd.DataFrame({'kelt_upper':kelt_upper, 'kelt_lower':kelt_lower})
		return kelt_data

	def MACD(data):
		ewm26 = data.Close.ewm(span=26, adjust=True, min_periods=20).mean()
		ewm12 = data.Close.ewm(span=20, adjust=True, min_periods=20).mean()
		ewm9 = data.Close.ewm(span=9, adjust=True, min_periods=20).mean()

		MACD = ewm12 - ewm26
		MACD_signal = ewm = MACD.ewm(span=20, adjust=True, min_periods=20).mean()
		MACD_hist = MACD - MACD_signal

		MACD = pd.DataFrame({'MACD': MACD, 'MACD_signal': MACD_signal, 'MACD_hist': MACD_hist})
		return MACD

	def rsi(data):
		window_length =14
		close = data['Close']
		# Get the difference in price from previous step
		delta = close.diff()
		# Get rid of the first row, which is NaN since it did not have a previous
		# row to calculate the differences
		delta = delta[1:]
		# Make the positive gains (up) and negative gains (down) Series
		up, down = delta.copy(), delta.copy()
		up[up < 0] = 0
		down[down > 0] = 0
		# Calculate the EWMA
		roll_up1 = up.ewm(min_periods=14,span=14,adjust=False).mean()
		roll_down1 = down.abs().ewm(min_periods=14,span=14,adjust=False).mean()
		# Calculate the RSI based on EWMA
		RS1 = roll_up1 / roll_down1
		RSI1 = 100.0 - (100.0 / (1.0 + RS1))
		RSI = pd.DataFrame({'RSI': RSI1})
		return RSI
	
	
	def psar(data):
		iaf = 0.02
		maxaf = 0.2
		length = len(data)
		dates = list(data.index)
		high = list(data['High'])
		low = list(data['Low'])
		close = list(data['Close'])
		psar = close[0:len(close)]
		psarbull = [None] * length
		psarbear = [None] * length
		bull = True
		af = iaf
		ep = low[0]
		hp = high[0]
		lp = low[0]
		for i in range(2,length):
			if bull:
				psar[i] = psar[i - 1] + af * (hp - psar[i - 1])
			else:
				psar[i] = psar[i - 1] + af * (lp - psar[i - 1])
			reverse = False
			if bull:
				if low[i] < psar[i]:
					bull = False
					reverse = True
					psar[i] = hp
					lp = low[i]
					af = iaf
			else:
				if high[i] > psar[i]:
					bull = True
					reverse = True
					psar[i] = lp
					hp = high[i]
					af = iaf
			if not reverse:
				if bull:
					if high[i] > hp:
						hp = high[i]
						af = min(af + iaf, maxaf)
					if low[i - 1] < psar[i]:
						psar[i] = low[i - 1]
					if low[i - 2] < psar[i]:
						psar[i] = low[i - 2]
				else:
					if low[i] < lp:
						lp = low[i]
						af = min(af + iaf, maxaf)
					if high[i - 1] > psar[i]:
						psar[i] = high[i - 1]
					if high[i - 2] > psar[i]:
						psar[i] = high[i - 2]
			if bull:
				psarbull[i] = psar[i]
			else:
				psarbear[i] = psar[i]

		PSAR = pd.DataFrame({'Date': dates, "psar":psar, "psarbear":psarbear, "psarbull":psarbull})
		PSAR = PSAR.set_index('Date')
		# print(PSAR)
		return PSAR

class data_set:
	def calculate_indicators(data):
		#indicator_data = pd.DataFrame(data)
		indicator_data = pd.concat([data, indicators.Moving_Average(data), 
										indicators.ExpMovingAverage(data), 
										indicators.rsi(data),
										indicators.MACD(data),
										indicators.psar(data)
										], axis=1)
		indicator_data = indicator_data.sort_values(by=['time'])
		return indicator_data
			
# def main():
	# url = "https://api-fxtrade.oanda.com/v1/candles?instrument=AUD_USD&count=5000&candleFormat=midpoint&granularity=D&dailyAlignment=0&alignmentTimezone=America%2FNew_York" 
	# data = collect_data.get_data(url)
	# print(data)
	# full_data = data_set.build_data_set(data)
	# full_data.to_csv('indicator_data.csv')
	# print(full_data)
	# return full_data
	
	# print(data.dtypes)
 
    
# main()



