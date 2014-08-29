

import TwitterAPI



OAUTH_TOKEN  = "2774014044-DZzD9XdHmosQ2RkShOLxDmNeJmQarkMEtBhkUkb"
OAUTH_SECRET = "tbzwql6tw9fTkfx5ayZcg80vCcd9YZHNFBeC9NJ6frmB4"
CONSUMER_KEY = "MNpC4O4mlXh6yIePNFGNfbsEm"
CONSUMER_SECRET = "ASIhfYd0HgQta5OEub4FklXOCKugGPjbqAWrs78n9Y9IdBZTQN"



from TwitterAPI import TwitterAPI
api = TwitterAPI(CONSUMER_KEY , CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET)

if __name__ == "__main__":

	r = api.request('search/tweets', {'q':'#python', 'count': 2 })
	c = 10
	for item in r:
		print(item['text'] if 'text' in item else item)