import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob
import text2emotion as te
import preprocessor as p
import matplotlib.pyplot as plt


#pip install tweet-preprocessor

class TwitterClient(object): 
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
		''' 
		Class constructor or initialization method. 
		'''
		# keys and tokens from the Twitter Dev Console 
		consumer_key = '7oJ01VBX8IVajacqdY7UJNJOC'
		consumer_secret = 'jYRUm0jZQzZf05NUErivVDFaD46RVsVm1N02lneYSJrJ3FxEBj'
		access_token = '87909508-jNHt8bv6ZnpmPiqaz72hsnGOLGARtgoL7kqPGCZ9p'
		access_token_secret = 'IU6MVyWA6f1Vljlm3a0s1nYbTSvd6KJoA0uvwhaDZHZzl'

		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
		''' 
		Utility function to classify sentiment of passed tweet 
		using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet))
		
		#nltk is the method original: nlp		
		#present in textblob
		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 10): 
		''' 
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = [] 

		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count) 

			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 

				# saving text of tweet 
				parsed_tweet['text'] = tweet.text 
				# saving sentiment of tweet 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e)) 

def main(): 
	# creating object of TwitterClient Class 
	api = TwitterClient() 
	# calling function to get tweets 
	tweets = api.get_tweets(query = 'Donald Trump', count = 100) 

	# picking positive tweets from tweets 
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 

	# percentage of positive tweets 
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
	p1 = format(100*len(ptweets)/len(tweets))
	# picking negative tweets from tweets 
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
	# percentage of negative tweets 
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
	n = format(100*len(ntweets)/len(tweets))
	# percentage of neutral tweets 
	print("Neutral tweets percentage: {} % \ ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))) 
	n1 = format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))
	
	y = [p1,n,n1]
	x = ["positive", "negative", "neutral"]
	plt.scatter(x, y)#, align='center')
	plt.ylabel('Y axis')
	plt.xlabel('X axis')
	plt.show()



	# printing first 5 positive tweets 
	print("\n\nPositive tweets:") 
	for tweet in ptweets[:5]: 
		text = p.clean(tweet['text'])
		print(text)
		print(te.get_emotion(text))

	# printing first 5 negative tweets 
	print("\n\nNegative tweets:") 
	for tweet in ntweets[:5]: 
		#print(tweet['text'])
		text = p.clean(tweet['text'])
		print(text)
		print(te.get_emotion(text))
		#tweetn = TextBlob(self.clean_tweet(tweet['text']))
		#te.get_emotion(tweetn['text'])
	
	#tweet = TextBlob(self.clean_tweet(tweet))
	#te.get_emotion(tweet)
	
	
	#y = [p1,n,n1]
	#x = ["positive", "negative", "neutral"]
	#plt.scatter(x, y)#, align='center')
	#plt.ylabel('Y axis')
	#plt.xlabel('X axis')
	#plt.show()


if __name__ == "__main__": 
	# calling main function 
	main() 
