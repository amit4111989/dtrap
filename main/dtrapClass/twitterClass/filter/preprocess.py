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
 
def get_tokens(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    
    tweet = [term for term in tokens ]
    return tweet
    
def get_features(s):
    features = {}
    x = word_features(s)
    y = bigram_word_features(s)
    features = x.copy()
    features.update(y)
    
    return features