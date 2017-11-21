############main.py##############
###Michael Ennis Final Project###
#CS496 - Oregon State University#
########## 11/19/2017 ###########

from google.appengine.ext import ndb
from datetime import datetime
import webapp2
import json
import hashlib
import urllib2

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

#START ACCOUNT DEFINITION#
class Account(ndb.Model):
	id = ndb.StringProperty()
	owner = ndb.StringProperty()
	coin = ndb.StringProperty(required=True)
	type = ndb.StringProperty()
	date = ndb.StringProperty()
	price = ndb.IntegerProperty()
	amount = ndb.IntegerProperty()
	total = ndb.IntegerProperty()
#END ACCOUNT DEFINITION#

#START COIN DEFINITION#
class Coin(ndb.Model):
	id = ndb.StringProperty()
	market = ndb.StringProperty()
	high = ndb.IntegerProperty()
	low = ndb.IntegerProperty()
	last = ndb.IntegerProperty()
#END COIN DEFINITION#

#START BUY HANDLER#
class BuyHandler(webapp2.RequestHandler):
	def post(self, id=None):
		if id:
			buy_data = json.loads(self.request.body)
			account = getAccount(id)
			coin = buy_data['coin']
			checker = checkCoin(coin)
			if((account is not "error") and (checker is 1)):
				new_buy = Account()
				new_buy.owner = account
				new_buy.coin = buy_data['coin']
				new_buy.type = "buy"
				new_buy.date = buy_data['date']
				new_buy.price = buy_data['price']
				new_buy.amount = buy_data['amount']
				new_buy.total = buy_data['price'] * buy_data['amount']
				new_buy.put()
				new_buy.id = new_buy.key.urlsafe()
				new_buy.put()
				buy_dict = new_buy.to_dict()
				buy_dict['self'] = '/buy/' + new_buy.key.urlsafe()
				self.response.write(json.dumps(buy_dict))
			else:
				self.response.set_status(403)
		else:
			self.response.set_status(400)
			
	def get(self,id=None):
		if id:
			accountid = getAccount(id)
			buyList = list()
			accounts = Account.query(Account.owner == accountid)
			for account in accounts:
				if(account.type == "buy"):
					buy_dict = account.to_dict()
					#buy_dict['self'] = '/buy/' + Account.key.urlsafe()
					buyList.append(buy_dict)
			self.response.write(json.dumps(buyList))
		else:
			self.response.set_status(400)
			
	def patch(self, id=None):
		if id:			
			try:
				buy_data = ndb.Key(urlsafe=id).get()
			except Exception:
				buy_data = None
			if buy_data is None:
				self.response.set_status(400)
			else:
				patch_data = json.loads(self.request.body)
				if 'date' in patch_data:
					buy_data.date = patch_data['date']
					buy_data.put()
				if 'price' in patch_data:
					buy_data.price = patch_data['price']
					buy_data.put()
				if 'amount' in patch_data:
					buy_data.amount = patch_data['amount']
					buy_data.put()
				buy_data.total = buy_data.price * buy_data.amount
				buy_data.put()
				buy_dict = buy_data.to_dict()
				buy_dict['self'] = '/buy/' + buy_data.id
				self.response.write(json.dumps(buy_dict))
		else:
			self.response.set_status(400)
			
	def delete(self, id=None):
		if id:
			try:
				buy_to_delete = ndb.Key(urlsafe=id).get()
			except Exception:
				buy_to_delete = None
			if buy_to_delete is None:
				self.response.set_status(400)
			else:
				buy_to_delete.key.delete()
				self.response.set_status(204)			
		else:
			self.response.set_status(400)			
#END BUY HANDLER#

#START SELL HANDLER#
class SellHandler(webapp2.RequestHandler):
	def post(self, id=None):
		if id:
			sell_data = json.loads(self.request.body)
			account = getAccount(id)
			coin = sell_data['coin']
			checker = checkCoin(coin)
			if((account is not "error") and (checker is 1)):
				new_sell = Account()
				new_sell.owner = account
				new_sell.coin = sell_data['coin']
				new_sell.type = "sell"
				new_sell.date = sell_data['date']
				new_sell.price = sell_data['price']
				new_sell.amount = sell_data['amount']
				new_sell.total = sell_data['price'] * sell_data['amount']
				new_sell.put()
				new_sell.id = new_sell.key.urlsafe()
				new_sell.put()
				sell_dict = new_sell.to_dict()
				sell_dict['self'] = '/sell/' + new_sell.key.urlsafe()
				self.response.write(json.dumps(sell_dict))
			else:
				self.response.set_status(403)
		else:
			self.response.set_status(400)
			
	def get(self,id=None):
		if id:
			accountid = getAccount(id)
			sellList = list()
			accounts = Account.query(Account.owner == accountid)
			for account in accounts:
				if(account.type == "sell"):
					sell_dict = account.to_dict()
					#buy_dict['self'] = '/buy/' + Account.key.urlsafe()
					sellList.append(sell_dict)
			self.response.write(json.dumps(sellList))
		else:
			self.response.set_status(400)
			
	def patch(self, id=None):
		if id:			
			try:
				sell_data = ndb.Key(urlsafe=id).get()
			except Exception:
				sell_data = None
			if sell_data is None:
				self.response.set_status(400)
			else:
				patch_data = json.loads(self.request.body)
				if 'date' in patch_data:
					sell_data.date = patch_data['date']
					sell_data.put()
				if 'price' in patch_data:
					sell_data.price = patch_data['price']
					sell_data.put()
				if 'amount' in patch_data:
					sell_data.amount = patch_data['amount']
					sell_data.put()
				sell_data.total = sell_data.price * sell_data.amount
				sell_data.put()
				sell_dict = sell_data.to_dict()
				sell_dict['self'] = '/sell/' + sell_data.id
				self.response.write(json.dumps(sell_dict))
		else:
			self.response.set_status(400)
			
	def delete(self, id=None):
		if id:
			try:
				sell_to_delete = ndb.Key(urlsafe=id).get()
			except Exception:
				sell_to_delete = None
			if sell_to_delete is None:
				self.response.set_status(400)
			else:
				sell_to_delete.key.delete()
				self.response.set_status(204)			
		else:
			self.response.set_status(400)
#END SELL HANDLER#

#START BALANCE HANDLER#
class BalanceHandler(webapp2.RequestHandler):
	def get(self, id=None):
		if id:
			self.response.set_status(400)
		else:
			self.response.set_status(400)
#END BALANCE HANDLER#

#START ACCOUNT HANDLER#
def getAccount(token):	
	# Set up the header string for requesting information.
	#auth_header = 'Bearer ' + token
	
	#headers = {
	#	'Authorization' : auth_header
	#}
	
	# Request the profile information, store in json. 
	#result = urlfetch.fetch(url="https://www.googleapis.com/plus/v1/people/me", headers = headers, method=urlfetch.GET)
	# Pause or results are processed before they are received.
	#time.sleep(0.5)
	#results = json.loads(result.content)
	
	# Check if user is a Google Plus user
	#isPlusUser = results['isPlusUser']
	
	# Error code to send back. 
	#errorCode = "error"
		
	#If the user is a plus user, display information.
	#if(isPlusUser):
	#	name = results['name']['givenName'] + results['name']['familyName']
	#	hash_object = hashlib.sha256(name)
	#	hex_dig = hash_object.hexdigest()
	#	return hex_dig
	#else:
	#	return errorCode
	
	hash_object = hashlib.sha256(token)
	hex_dig = hash_object.hexdigest()
	return hex_dig
#END ACCOUNT HANDLER#

#START COIN HANDLER#
class CoinHandler(webapp2.RequestHandler):
	def post(self, id=None):
		coin_data = json.loads(self.request.body)		
		new_coin = Coin()
		new_coin.market = coin_data['market']
		new_coin.high = 0
		new_coin.low = 0
		new_coin.last = 0
		new_coin.put()
		new_coin.id = new_coin.key.urlsafe()
		new_coin.put()
		coin_dict = new_coin.to_dict()
		coin_dict['self'] = '/coin/' + new_coin.key.urlsafe()
		self.response.write(json.dumps(coin_dict))
#END COIN HANDLER#

#START CHECK COIN#
def checkCoin(coinCheck):
	coins = Coin.query(Coin.market == coinCheck).get()
	if coins is None:
		return 0
	else:
		return 1
#END CHECK COIN#

#START UPDATE COIN DATABASE#
def updateCoin():
	content = urllib2.urlopen("https://bittrex.com/api/v1.1/public/getmarketsummaries").read()
	coins = Coin.query()
	for result in content:
		if(content['result']['MarketName'] in coinList):
			coin = content['result']['MarketName']
			for coin in coins:
				if(coin == coins.market):
					coins.high = content['result']['High']
					coins.low = content['result']['Low']
					coins.last = content['result']['Last']
					coins.put()
#END UPDATE COIN DATABASE#

#START INITIALIZE COINS#
def initializeCoins():
	content = urllib2.urlopen("https://bittrex.com/api/v1.1/public/getmarketsummaries")
	json_object = json.load(content)

	for i in json_object['result']:
		new_coin = Coin()
		new_coin.market = i['MarketName']
		new_coin.high = Decimal(i['High'])
		new_coin.low = Decimal(i['Low'])
		new_coin.last = Decimal(i['Last'])
		new_coin.put()
		new_coin.id = new_coin.key.urlsafe()
		new_coin.put()
		coin_dict = new_coin.to_dict()
		coin_dict['self'] = '/coin/' + new_coin.key.urlsafe()
		
#END INITIALIZE COINS#

#START MAINPAGE#
class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write('Hello')
		
	def post(self):
		initializeCoins()

#END MAINPAGE#

#START APP#
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/buy/(.*)', BuyHandler),
	('/sell/(.*)', SellHandler),
	('/balance/(.*)', BalanceHandler),
	('/coin(.*)', CoinHandler)
], debug=True)
#END APP#