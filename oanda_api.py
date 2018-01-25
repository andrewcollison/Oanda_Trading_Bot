import json

import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.accounts as accounts

import oandapyV20.endpoints.orders as orders
import oandapyV20
import pandas as pd



accountID = '101-011-7588716-002'
access_token = '5514b7cdb3e93d9506ecc8a87fa51254-9264c6dddb5f557577541c058ee28d55'
client = oandapyV20.API(access_token=access_token)


class accsum:
	def account_value():
		client = oandapyV20.API(access_token=access_token)
		r = accounts.AccountSummary(accountID)
		client.request(r)
		return r.response['account']['balance']
		
	def prof_loss():
		client = oandapyV20.API(access_token=access_token)
		r = accounts.AccountSummary(accountID)
		client.request(r)
		return r.response['account']['pl']
		
	def open_positions(shortlong):
		r = positions.OpenPositions(accountID=accountID)
		client = oandapyV20.API(access_token=access_token)
		client.request(r)
		pos_lst = r.response['positions'][-1]
		return pos_lst[shortlong]['units']

class buy_sell:
		def mkt_position(instrument, units):
			data = {"order": {
						"instrument": instrument,
						"units": units,
						"type": "MARKET",
						"positionFill": "DEFAULT"
						}
					}
			client = oandapyV20.API(access_token=access_token)
			r = orders.OrderCreate(accountID, data=data)
			client.request(r)
			# print(r.response)
			
		def close_all(shortlong, instrument):
			if shortlong == 'short':
				data ={ "shortUnits": "ALL" }
			elif shortlong == 'long':
				data = { "longUnits": "ALL" }				
			
			r = positions.PositionClose(accountID=accountID, instrument=instrument, data=data)
			client.request(r)
			# print(r.response)
			

# buy_sell.mkt_position('AUD_USD', '-1')
# print(accsum.account_value())
# print(accsum.prof_loss())
# print(accsum.open_positions('long'))


# buy_sell.close_all('long', 'AUD_USD')