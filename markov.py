from __future__ import division
import tweepy
import random
from collections import defaultdict

consumer_key = "BVCoUsXsawKsk5XheX1LOkmOZ"
consumer_secret = "6VRN1kmBM8c5br6ARmsG1VKjBMAhsfO8DmEo3kZo1vkU3NbTOd"

access_token = "178212768-NYRICrlDkYJpZPJoOOMW9WGF74YdveRvK7dKVwwo"
access_token_secret = "DgGSwG9jyVZIsGGM5Jup9nC7SO8s8RFJEoD5utsDmUid3"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.user_timeline("djkhaled", count=500)


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


tweets = [tweet.text for tweet in public_tweets]

markov = defaultdict(lambda: defaultdict(lambda: 0))
grams = set()

total_grams = 0

# simple markov chain
for tweet in tweets:
	words = tweet.split()
	for i in range(len(words)-2):
		subtweet = tuple(words[i:i+3])
		grams.add(subtweet)
		markov[subtweet[:2]][subtweet[2]] = markov[subtweet[:2]][subtweet[2]] + 1
		total_grams = total_grams + 1

# initial state
initial = random.sample(grams, 1)[0]

word1 = initial[0]
word2 = initial[1]
word3 = None

tweet = ""
tweet = tweet + word1 + " " + word2

max_iter = 140

while max_iter > 0:
	# Find a third word
	t = (word1, word2)

	possibilities = markov[t]
	if not possibilities:
		# no possibilities, go random
		break
	else:
		flat = [(word, possibilities[word]) for word in possibilities]
		accum = 0
		maxValue = 0
		for i in range(len(flat)):
			(word, count) = flat[i]
			flat[i] = (word, count + accum)
			accum = accum + count
			maxValue = accum
		selection = random.randint(0, maxValue)
		for i in range(len(flat)):
			(word, count) = flat[i]
			if selection <= count:
				# select this one
				word3 = word
				break

		tweet = tweet + " " + word3

	word1 = word2
	word2 = word3
	word3 = None
	max_iter = max_iter - 1

print "Tweet: "
print tweet


