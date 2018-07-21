import pandas as pd
import numpy as np
import get_data
from get_data import indicators
import matplotlib.pyplot as plt
plt.style.use('ggplot')

instrument = "USD_JPY"
stratergy = "50-200d MA Crossover"
# data = get_data.collect_data.get_data(instrument)
# data.to_csv('pair_data.csv')
data = pd.read_csv("pair_data.csv", parse_dates = True)
## Bring in more indicators
data = data.set_index(data['time'])
data['50d'] = data['Close'].rolling(center=False, window=50).mean()
data['200d'] = data['Close'].rolling(center=False, window=200).mean()
data = data.dropna(axis=0, how='any')
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
		# port_val = list(data["Port_Value"])
		profit = list(data["Profit"])
		position = 0
		for i in range(len(date)):
			amount = 100
			# open_position_price = 0
			## Start long position
			if regime[i] == 1 and regime[i -1] !=1:
				open_position_price = close[i]
				print("Open Long")
				# long_position = amount*open_position_price
				# port_val[i] = port_val[i] - long_position				
				# print("Open Long:", close_price[i], date[i], port_val[i])		
			## Close long position
			elif regime[i] == -1 and regime[i -1] == 1:
				close_position_price = close[i] - open_position_price
				profit[i] = close_position_price*amount
				print("Close Long: Profit", profit[i])
				# close_long_position = (amount*close_price[i]) - (amount*open_position_price)
				# port_val[i] = port_val[i-1] + close_long_position
				# print("Close Long", close_price[i], date[i], port_val[i])
				
			# else:
				# profit[i] = 0
		print("Overall Profit:", np.cumsum(profit)[-1])	
			
				
		# result_data = pd.DataFrame({"date": date, "Close": close_price, "Port_Value": port_val, "Regime": regime})
		# print(result_data.head())
		# result_data[["date", "Port_Value"]].plot()
		# plt.show()
			
			
			# Start Short Position
			# if regime[i] == -1 and regime[i -1] !=-1:
				# open_price = close_price[i]
				# short_position = (amount*close_price[i]) 
				# port_val[i] = port_val[i] - position
				# print("Open Short:", close_price[i], date[i], port_val[i])
			# Close short position	
			# elif regime[i] == 1 and regime[i -1] == -1:
				# close_position = (amount*close_price[i]) - (amount*open_price)
				# port_val[i] = port_val[i-1] + close_position
				# print("Close Short:", close_price[i], date[i], port_val[i])
			# If signal is zero, portfolio maintains same price
			# else:
				# port_val[i] = port_val[i-1]


			
		# print("Value of long trades: $", port_val[-1])
		# plt.plot(date, port_val)
		# plt.show()
		
		

		
		
		
class visual:
			def graph_results(data):
				fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)
				data[["Close", "50d", "200d"]].plot(ax = axes[0])
				data["Regime"].plot(ax=axes[1])
				plt.show()
			
		
stratergy.Regime(data)
test_stratergy.trade(data)

# visual.graph_results(data)





		