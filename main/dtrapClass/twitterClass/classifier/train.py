import re
import cPickle
import json
import nltk
import ast
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures as BAM 
from itertools import chain 
import string
from collections import Counter

count_all = Counter()
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'I', "I'm"]

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def word_features(words):
    return dict((word, True) for word in words)

def bigram_word_features(words, score_fn=BAM.chi_sq, n=200):     
    bigram_finder = BigramCollocationFinder.from_words(words)     
    bigrams = bigram_finder.nbest(score_fn, n)     
    return dict((bg, True) for bg in chain(words, bigrams))
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def tweet_features(tweet_data):
    features = {}
    tweet = [term for term in preprocess(str(tweet_data['text'])) ]
    
    #tags = nltk.pos_tag(tweet)
    #for tag in tags:
    #    features['contains('+str(tag)+')'] = True
    
    x = word_features(tweet)
    y = bigram_word_features(tweet)
    
    features = x.copy()
    features.update(y)
    
    #for ngrams in nltk.ngrams(tweet, 3):
    #    features['contains(%s)' % ','.join(ngrams)] = True
    #tweet = ' '.join(tweet)
    
    # for bigrams in nltk.bigrams(tweet):
    #     features['contains(%s)' % ','.join(bigrams)] = True
    
    # for ngrams in nltk.ngrams(tweet,1):
    #     features['contains(%s)' % ','.join(ngrams)] = True
        
    # for ngrams in nltk.ngrams(tweet, 3):
    #      features['contains(%s)' % ','.join(ngrams)] = True
    # print features
    return features
 
tweet = "RT @marcobonzanini: just an example! :D http://example.com #NLP"

file = open('tweets.p')
tweets = cPickle.load(file)
file.close()

terms = []

train_set = []
for tweet in tweets:
        # print str(tweet['text'])
        #temp = [term for term in preprocess(str(tweet['text'])) if term not in stop]
        #for i in temp:
        #    terms.append(i)
    try:
        tweet = ast.literal_eval(tweet)
        a = str(tweet['text'])
    except:
        continue
    else:
        features = tweet_features(tweet)
        train_set.append((features,tweet['valid']))
    
classifier = nltk.NaiveBayesClassifier
classifier = nltk.NaiveBayesClassifier.train(train_set)

with open('classifier.p','w+') as f:
    cPickle.dump(classifier,f)
    f.close()

file = open('test_tweets.p')
test_tweet= cPickle.load(file)
file.close()

test_set = []
correct_count = 0
fail_count = 0
false_positive = 0
true_negative = 0
positives = 0

for i in test_tweet:
    try:
        tweet = ast.literal_eval(i)
        a = str(tweet['text'])
        features = tweet_features(tweet)
        guess = classifier.classify(features)
        
        if tweet['valid']==1:
            positives+=1
        
        if tweet['valid']==guess:
            correct_count += 1
        else:
            if tweet['valid']==1:
                true_negative+=1
            else:
                false_positive+=1
            print tweet['text']
            print guess
            fail_count += 1
    except:
        continue

#print terms
print correct_count , fail_count
print true_negative , false_positive
print positives
count_all.update(terms)
#print(count_all.most_common(5))

