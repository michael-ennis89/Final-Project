############main.py##############
###Michael Ennis Final Project###
#CS496 - Oregon State University#
########## 11/19/2017 ###########

from google.appengine.ext import ndb
from datetime import datetime
from google.appengine.api import users
from google.appengine.api import urlfetch
import webapp2
import json
import hashlib
import urllib2
import logging
import os
import urllib
import jinja2
import time

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
	
#START ACCOUNT DEFINITION#
class Account(ndb.Model):
	id = ndb.StringProperty()
	owner = ndb.StringProperty()
	coin = ndb.StringProperty(required=True)
	type = ndb.StringProperty()
	date = ndb.StringProperty()
	price = ndb.FloatProperty()
	amount = ndb.FloatProperty()
	total = ndb.FloatProperty()
#END ACCOUNT DEFINITION#

#START COIN DEFINITION#
class Coin(ndb.Model):
	id = ndb.StringProperty()
	market = ndb.StringProperty()
	high = ndb.FloatProperty()
	low = ndb.FloatProperty()
	last = ndb.FloatProperty()
#END COIN DEFINITION#

#START STATE DEFINITION#	
class State(ndb.Model):
	id = ndb.StringProperty(),
	state = ndb.StringProperty()
#END STATE DEFINITION

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
				new_buy.price = float(buy_data['price'])
				new_buy.amount = float(buy_data['amount'])
				new_buy.total = float(buy_data['price']) * float(buy_data['amount'])
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
					buy_data.price = float(patch_data['price'])
					buy_data.put()
				if 'amount' in patch_data:
					buy_data.amount = float(patch_data['amount'])
					buy_data.put()
				buy_data.total = float(buy_data.price) * float(buy_data.amount)
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
				new_sell.price = float(sell_data['price'])
				new_sell.amount = float(sell_data['amount'])
				new_sell.total = float(sell_data['price']) * float(sell_data['amount'])
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
					sell_data.price = float(patch_data['price'])
					sell_data.put()
				if 'amount' in patch_data:
					sell_data.amount = float(patch_data['amount'])
					sell_data.put()
				sell_data.total = float(sell_data.price) * float(sell_data.amount)
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
			updateCoin()
			accountid = getAccount(id)
			accountList = list()
			accounts = Account.query(Account.owner == accountid)
			for account in accounts:
				if account.type == "buy":
					coin_to_update = Coin.query(Coin.market == account.coin).get()
					new_price = float(coin_to_update.last) * float(account.amount)
					old_cost = float(account.total)
					updated_balance = float(new_price) - float(old_cost)
					new_coin = [account.coin, updated_balance]
					accountList.append(new_coin)
				else:
					coin_to_update = Coin.query(Coin.market == account.coin).get()
					new_price = float(coin_to_update.last) * float(account.amount)
					old_cost = float(account.total)
					updated_balance = float(old_cost) - float(new_price)
					new_coin = [account.coin, updated_balance]
					accountList.append(new_coin)
			balance = {}
			for cur, val in accountList:
				if cur in balance:
					balance[cur] += val
				else:
					balance[cur] = val
					
			self.response.write(json.dumps(balance))
		else:
			self.response.set_status(400)
#END BALANCE HANDLER#

#START ACCOUNT HANDLER#
def getAccount(token):	
	#Set up the header string for requesting information.
	auth_header = 'Bearer ' + token
	
	headers = {
		'Authorization' : auth_header
	}
	
	#Request the profile information, store in json. 
	result = urlfetch.fetch(url="https://www.googleapis.com/plus/v1/people/me", headers = headers, method=urlfetch.GET)
	#Pause or results are processed before they are received.
	time.sleep(0.5)
	results = json.loads(result.content)
	#Check if user is a Google Plus user
	isPlusUser = results['isPlusUser']
	
	#Error code to send back. 
	errorCode = "error"
		
	#If the user is a plus user, display information.
	if(isPlusUser):
		url = results['url']
		hash_object = hashlib.sha256(url)
		hex_dig = hash_object.hexdigest()
		return hex_dig
	else:
		return errorCode
	
	#hash_object = hashlib.sha256(token)
	#hex_dig = hash_object.hexdigest()
	#return hex_dig
#END ACCOUNT HANDLER#

#START CHECK COIN#
def checkCoin(coinCheck):
	coins = Coin.query(Coin.market == coinCheck).get()
	if coins is None:
		return 0
	else:
		return 1
#END CHECK COIN#

#START INITIALIZE OR UPDATE COINS PRICES#
def updateCoin():
	content = urllib2.urlopen("https://bittrex.com/api/v1.1/public/getmarketsummaries")
	json_object = json.load(content)

	for i in json_object['result']:
		if "USDT" in i['MarketName']:
			coin_to_update = Coin.query(Coin.market == i['MarketName']).get()
			if coin_to_update is None:
				new_coin = Coin()
				new_coin.market = i['MarketName']
				new_coin.high = float(i['High'])
				new_coin.low = float(i['Low'])
				new_coin.last = float(i['Last'])
				new_coin.put()
				new_coin.id = new_coin.key.urlsafe()
				new_coin.put()
				coin_dict = new_coin.to_dict()
				coin_dict['self'] = '/coin/' + new_coin.key.urlsafe()
			else:
				coin_to_update.high = float(i['High'])
				coin_to_update.low = float(i['Low'])
				coin_to_update.last = float(i['Last'])
				coin_to_update.put()
	
		
#END INITIALIZE OR UPDATE COINS PRICES#

# [START MAINPAGE]
class MainPage(webapp2.RequestHandler):
	def get(self):
		# Create a state variable and set it in the template values object to pass to JINJA.
		state = hashlib.sha256(os.urandom(256)).hexdigest()
		template_values = {
			'state' : state
		}
		
		# Create new State object and store it in database.
		newkey = State(id="", state=state)
		newkey.put()
		newkey.id = str(newkey.key.id())
		newkey.put()
		
		# Display the index.html page with Jinja variables. 
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))
# [END MAINPAGE]

# [START OauthHandler]
class OauthHandler(webapp2.RequestHandler):
	def get(self):
		# Request the state and code from webapp2
		state = self.request.get('state')
		code = self.request.get('code')
		verification = 0;
		
		#query to get a list of all the states.
		check_state = State.query()
		results = check_state.fetch()
		#find the state variable and delete it with the id set verification to true.
		for i in results:
			if (i.state == state):
				verification = 1
				ndb.Key("State", long(i.key.id())).delete()
				
		# If the state is found
		if (verification == 1):
			# My client id, secret, and redirec_uri
			client_id = "1024414908095-7rdg82irp2utqa49sjnoj3h26f7mmoo3.apps.googleusercontent.com"
			client_secret = "QZ0c3oKYA1LdAU2BCWVzu44D"
			redirect_uri = "https://coinaccountosu-186723.appspot.com/oauth"
			
			# Load users code and my info into a payload to request the token. 
			payload = {
			'code' : code,
			'client_id' : client_id,
			'client_secret' : client_secret,
			'redirect_uri' : redirect_uri,
			'grant_type' : 'authorization_code'
			}
			
			# Request the token, store in JINJA2 template_values
			payload = urllib.urlencode(payload)
			tokenFetch = urlfetch.fetch(url="https://www.googleapis.com/oauth2/v4/token", payload = payload, method=urlfetch.POST)
			# Pause or results are processed before they are received. 
			time.sleep(0.5)
			results = json.loads(tokenFetch.content)
			token = results['access_token']
			
			template_values = {
				'state' : state,
				'token' : token
			}

			# Display oauth.html page with JINJA variables
			template = JINJA_ENVIRONMENT.get_template('oauth.html')
			self.response.write(template.render(template_values))
		# Else display error bad request 
		else:
			self.response.write('400 Bad Request')
			self.response.set_status(400)
# [END OauthHandler]

# [START DisplayHandler]
class DisplayHandler(webapp2.RequestHandler):
	def post(self):
		# Request the state and code from webapp2
		state = self.request.get('state')
		token = self.request.get('token')
		
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
		
		#If the user is a plus user, display information.
		if(isPlusUser):
			# Grab the required variables from the json and place in template.
			givenName = results['name']['givenName']
			familyName = results['name']['familyName']
			urls = results['url']
			
			template_values = {
				'firstName' : givenName,
				'lastName' : familyName,
				'url' : urls,
				'token' : token
			}
			
			template = JINJA_ENVIRONMENT.get_template('display.html')
			self.response.write(template.render(template_values))
		# Else display 400 Bad Request error
		else:
			self.response.write('400 Bad Request')
			self.response.set_status(400)
# [END DisplayHandler]

#START APP#
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/buy/(.*)', BuyHandler),
	('/sell/(.*)', SellHandler),
	('/balance/(.*)', BalanceHandler),
	('/oauth', OauthHandler),
	('/display', DisplayHandler)
], debug=True)
#END APP#