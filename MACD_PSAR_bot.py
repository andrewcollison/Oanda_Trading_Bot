import pandas as pd
import get_data 
import time
from oanda_api import buy_sell, accsum

buy_sell.mkt_position('AUD_USD', '-1')
current_status = 0 # 1 = in long position, 0 = in sort position
print('This is where the fun begins')
while True:
	instrument = "AUD_USD"
	df = get_data.main()
	account_value = accsum.account_value()
	units = round((0.04*float(account_value))/df['Close'].iloc[-1])		
	
	if df['psarbull'].iloc[-1] != "NaN":
		if current_status == 0:
			current_status = 1
			print('Buy Signal')
			buy_sell.close_all('short', 'AUD_USD')
			time.sleep(5)
			buy_sell.mkt_position('AUD_USD', str(units))
		
	elif df['psarbear'].iloc[-1] != "NaN":
		if current_status == 1:
			current_status = 0
			print('Sell Signal')
			buy_sell.close_all('long', 'AUD_USD')
			time.sleep(5)
			buy_sell.mkt_position('AUD_USD', str(-units))
		
	
	print(current_status)
	time.sleep(5)

