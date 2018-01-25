import pandas as pd
import numpy as np
import get_data
import matplotlib.pyplot as plt
plt.style.use('ggplot')


instrument = "USD_JPY"
stratergy = "50-200d MA Crossover"
data = get_data.collect_data.get_data(instrument)
# data.to_csv('pair_data.csv')
# data = pd.read_csv("pair_data.csv", parse_dates = True)

##Calculating the moving averages
data = data.set_index(data['time'])
data['50d'] = data['Close'].rolling(center=False, window=50).mean()
data['200d'] = data['Close'].rolling(center=False, window=200).mean()
data["42-252"] = data["50d"] - data["200d"]


## This is the trading stratergy
data["Regime"] = np.where(data["50d"] > data["200d"], 1, 0) # by long
data["Regime"] = np.where(data["50d"] < data["200d"], -1, data["Regime"]) # sell short
print(data["Regime"].value_counts())

data['Market'] = np.log(data["Close"] / data["Close"].shift(1))
data["Stratergy"] = data["Regime"].shift(1) * data["Market"]

data["Market"] = data["Market"].cumsum().apply(np.exp)
data["Stratergy"] = data["Stratergy"].cumsum().apply(np.exp)


## Visulaize the Results
fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)
data[["Close", "50d", "200d" ]].plot(ax = axes[0])
data["Regime"].plot(ax=axes[1])
data[["Stratergy", "Market"]].plot(ax = axes[2])
axes[0].set_title("Backtest: Instrument: {} : Stratergy: {}".format(instrument, stratergy))
axes[1].set_title("Long/Short/Neutral Position")
axes[2].set_title("Relative Returns of Stratergy Vs Market")
plt.show()







