from langdetect import detect
import langdetect
import json
import langid

detectscore = {}
langidscore = {}
tweetwords = {}
i = 0
with open("tweets.json", "r") as tweets:
	for line in tweets:
		tweet = json.loads(line)
		if i == 20:
			break
		i += 1
		wordlist = tweet["text"].split(" ")
		lang = tweet["lang"]
		for word in wordlist:
			print(word)
			# ternary expression doesn't work
			# tweetwords[word] = (tweetwords[word] + 1) if (word in tweetwords) else tweetwords[word]
			if word in tweetwords:
				tweetwords[word] += 1
			else:
				tweetwords[word] = 1
		try:
			withdetect = detect(tweet["text"])
			withlangid = langid.classify(tweet["text"])
			if withdetect in detectscore:
				detectscore[withdetect] += 1
			else:
				detectscore[withdetect] = 1
			if withlangid[0] in langidscore:
				langidscore[withlangid[0]] += 1
			else:
				langidscore[withlangid[0]] = 1
			#print(withdetect + " vs " + withlangid[0] + " vs " + tweet["lang"])
		except langdetect.lang_detect_exception.LangDetectException:
			pass
		
print(detectscore)
print(langidscore)
#print(tweetwords)
print(b'\x80abc'.decode("utf-8", "ignore"))
