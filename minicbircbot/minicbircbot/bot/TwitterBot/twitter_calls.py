
import TwitterAPI
from TwitterAPI import TwitterAPI




class TwitterCalls(object):

	def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
		self.api = TwitterAPI(consumer_key, consumer_secret, access_token , access_secret)




	def search(self, key, count):
		data =  self.api.request('search/tweets', {'q': key, 'count': count })
		return data.get_iterator()





