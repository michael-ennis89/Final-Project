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
	owner = ndb.StringProperty()
	id = ndb.StringProperty()
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
			
			if((account is not "error") and (checker is true)):
				new_buy = Account()
				new_buy.owner = account
				new_buy.id = new_buy.key.urlsafe()
				new_buy.coin = buy_data['coin']
				new_buy.type = "buy"
				new_buy.date = buy_data['date']
				new_buy.price = buy_data['price']
				new_buy.amount = buy_data['amount']
				new_buy.total = buy_data['price'] * buy_data['amount']
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
		else:
			self.response.set_status(400)
			
	def patch(self, id=None):
		if id:
		else:
			self.response.set_status(400)
			
	def delete(self, id=None):
		if id:
		else:
			self.response.set_status(400)			
#END BUY HANDLER#

#START SELL HANDLER#
class SellHandler(webapp2.RequestHandler):
	def post(self, id=None):
		if id:
		else:
			self.response.set_status(400)
			
	def get(self, id=None):
		if id:
		else:
			self.response.set_status(400)
			
	def patch(self, id=None):
		if id:
		else:
			self.response.set_status(400)
			
	def delete(self, id=None):
		if id:
		else:
			self.response.set_status(400)
#END SELL HANDLER#

#START BALANCE HANDLER#
class BalanceHandler(webapp2.RequestHandler):
#END BALANCE HANDLER#

#START ACCOUNT HANDLER#
def getAccount(token):	
		# Set up the header string for requesting information.
		auth_header = 'Bearer ' + token
		
		headers = {
			'Authorization' : auth_header
		}
		
		# Request the profile information, store in json. 
		result = urlfetch.fetch(url="https://www.googleapis.com/plus/v1/people/me", headers = headers, method=urlfetch.GET)
		# Pause or results are processed before they are received.
		time.sleep(0.5)
		results = json.loads(result.content)
		
		# Check if user is a Google Plus user
		isPlusUser = results['isPlusUser']
		
		# Error code to send back. 
		errorCode = "error"
		
		#If the user is a plus user, display information.
		if(isPlusUser):
			name = results['name']['givenName'] + results['name']['familyName']
			hash_object = hashlib.sha256(name)
			hex_dig = hash_object.hexdigest()
			return hex_dig
		else:
			return errorCode
#END ACCOUNT HANDLER#

#START CHECK COIN#
def checkCoin(coin):
	coins = Coin.query()
	if coins is None:
		initCoin()
		
	for coin in coins:
		if(coin == coins['market']):
			return true
	return false
#END CHECK COIN#

#START INITIALIZE COIN DATABASE#
def initCoin():
	coins = Coin.query()
	coinList = ["USDT-BTC", "USDT-NEO", "USDT_ETH", "USDT-BCC", "USDT-LTC", "USDT-LTC", "USDT-XRP", "USDT-OMG", "USDT-ETC", "USDT-ZEC", "USDT-DASH", "USDT-XMR"]
	if coins is None:
		content = urllib2.urlopen(https://bittrex.com/api/v1.1/public/getmarketsummaries).read()
		for result in content:
			if(content['result']['MarketName'] is in coinList):
				new_coin = Coin()
				new_coin.id = new_coin.key.urlsafe()
				new_coin.market = content['result']['MarketName']
				new_coin.high = content['result']['High']
				new_coin.low = content['result']['Low']
				new_coin.last = content['result']['Last']
				new_coin.put()
				coin_dict = new_coin.to_dict()
				coin_dict['self'] = '/coin/' + new_coin.key.urlsafe()			
#END INITIALIZE COIN DATABASE#

#START UPDATE COIN DATABASE#
def updateCoin():
coinList = ["USDT-BTC", "USDT-NEO", "USDT_ETH", "USDT-BCC", "USDT-LTC", "USDT-LTC", "USDT-XRP", "USDT-OMG", "USDT-ETC", "USDT-ZEC", "USDT-DASH", "USDT-XMR"]
	content = urllib2.urlopen(https://bittrex.com/api/v1.1/public/getmarketsummaries).read()
	coins = query.Coins()
	for result in content:
		if(content['result']['MarketName'] is in coinList):
			coin = content['result']['MarketName']
			for coin in coins:
				if(coin == coins.market):
					coins.high = content['result']['High']
					coins.low = content['result']['Low']
					coins.last = content['result']['Last']
					coins.put()
#END UPDATE COIN DATABASE#



#START MAINPAGE#
class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write('Hello')
#END MAINPAGE#

#START APP#
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/buy/(.*)', BuyHandler),
	('/sell/(.*)', SellHandler),
	('/balance/(.*)', BalanceHandler),
	('/coin/(.*)', CoinHandler)
], debug=True)
#END APP#