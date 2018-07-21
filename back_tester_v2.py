import pandas as pd
import numpy as np
import get_data
from get_data import indicators
import matplotlib.pyplot as plt
plt.style.use('ggplot')

## Gather the data
instrument = "USD_JPY"
stratergy = "50-200d MA Crossover"
# data = get_data.collect_data.get_data(instrument)
# data.to_csv('pair_data.csv')
# print(data)
data = pd.read_csv("pair_data.csv", parse_dates = True)

## Bring in more indicators
data = data.set_index(data['time'])
data['50d'] = data['Close'].rolling(center=False, window=7).mean()
data['200d'] = data['Close'].rolling(center=False, window=14).mean()
data = data.dropna(axis=0, how='any')
# print(data.head())

#### Portfolio Paramaters
data["Profit"] = 0
data["Regime"] = 0


class stratergy:	
	def Regime(data):		
		for index, row in data.iterrows():
			if row["50d"] > row["200d"]:
				# row["Regime"] = 1
				data.loc[index, "Regime"] = 1
				# print("Buy", index, row["Close"], row["Regime"])
			elif row["50d"] < row["200d"]:
				# row["Regime"] = -1
				data.loc[index, "Regime"] = -1
				# print("Sell", index, row["Close"], row["Regime"])
		print("These are the stratergy results: \n", data["Regime"].value_counts())
				
		
class test_stratergy:
	def trade(data):				
		date = list(data["time"])
		close = list(data["Close"])
		regime = list(data["Regime"])
		profit = list(data["Profit"])
		position = 0
		open_long_id = 0
		open_short_id = 0
		for i in range(len(date)):
			amount = 100
			# open_position_price = 0
			## Start long position
			if regime[i] == 1 and regime[i -1] !=1:
				open_long_id = i
				print("Open Long")		
			## Close long position
			elif regime[i] == -1 and regime[i -1] == 1:
				close_position_price = close[i] - close[open_long_id]
				profit[i] = close_position_price
				print("Close Long: Profit", profit[i])
				
			## Open short position
			elif regime[i] == -1 and regime[i -1] != -1:
				open_short_id = i
				print("Open Short")
			## Close short position
			elif regime[i] == 1 and regime[i -1] == -1:
				close_position_price = close[i] + close[open_short_id]
				profit[i] = close_position_price
				print("Close Short: Profit", profit[i])
				
				
		cum_profit = np.cumsum(profit)
		print("Overall Profit:", cum_profit[-1])	
		
		res_data = pd.DataFrame({"date":date, "profit": cum_profit})
		print(res_data.tail())
		res_data[["date", "profit"]].plot()
		plt.show()
		

class test_stratergy_2:
	def long_trades(data):
		date = list(data["time"])
		close = list(data["Close"])
		regime = list(data["Regime"])
		profit = list(data["Profit"])
		open_long_idx = 0
		close_long_idx = 0
		p_open = []
		p_close = []
		long_profit = 0
		in_trade = False

		for i in range(len(date)):
			if regime[i] == 1 and regime[i -1] !=1:
				open_long_idx = i
				p_open = close[i]
				in_trade = True
				print("Open Long: Price Open:", p_open, "Date:", date[i] )

			if regime[i] == -1 and regime[i-1] != -1:
				close_long_idx = i
				p_close = close[i]
				in_trade = False

				
				if regime[i]==1 and in_trade == True:
					print("Trade Still Open")
				
				long_profit = close[close_long_idx] - close[open_long_idx] 
				


				print("Close Long: Price Close:", p_close, "Profit",long_profit, "Date:", date[i] )


class test_stratergy_3:
	def long_trades(data):
		date = list(data["time"])
		close = list(data["Close"])
		regime = list(data["Regime"])
		profit = list(data["Profit"])
		open_idx = 0
		close_idx = 0
		p_open = []
		p_close = []
	
		# If final data point results in open trade
		# force the trade to close at the closing price
		if regime[-1] == 1:
			regime[-1] = -1
			# print(regime)

		for i in range(len(date)):
			if regime[i] == 1 and regime[i-1] == -1:
				open_idx = i
				print("Open Long: Price Open:", close[i]  , "Date:", date[i]  )

			if regime[i] == -1 and regime[i-1] == 1:
				profit[i] = (close[open_idx]/close[i])*100
				print("Close Long: Price Close:",close[i], "Profit:", profit[i], "Date:", date[i]  )
			
				
		cum_profit = np.cumsum(profit)
		print(cum_profit)






		
		
class visual:
			def graph_results(data):
				fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)
				data[["Close", "50d", "200d"]].plot(ax = axes[0])
				data["Regime"].plot(ax=axes[1])
				plt.show()
			
		
stratergy.Regime(data)
print(data.tail())

# test_stratergy.trade(data)
test_stratergy_3.long_trades(data)
# visual.graph_results(data)





		