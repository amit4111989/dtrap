from baseClass import Dtrap
from filter import preprocess
import re
import cPickle


class TwitterMain(Dtrap):
    
    classifier = ''
    keywords = {}
    keywords_re = ''
    blocked_keywords_re = ''
    
    def __init__(self):
        """
            Load data from files for constructor
            
        """
        self.load_objects()
        super(TwitterMain,self).__init__()
    
    def preprocess(self,text):
        """
            Break text into list of tokens following twitter norms
            
            Parameters:
            
                text : raw json text
            
        """
        return preprocess.get_tokens(text)
    
    def is_retweet(self,text):
        """
            Determin if tweet is a retweet
            
            Parameters:
            
                text : tokenized text from tweets
            
        """
        if text[0] == 'rt':
            return True
        else:
            return False
            
    def load_objects(self):
        """
            Load necessary data from files
            
        """
        
        # Load classifier
        with open('../twitterClass/classifier/classifier.p','r') as f:
            self.classifier = cPickle.load(f)
            
        #Load blocked keywords
        regex_str2 = []
        with open('../twitterClass/twitterMiningClass/private/blocked_keywords.txt','r') as f:
            keywords = f.read().split('\n')
            for key in keywords:
                key = key.split(',')
                #key[0] = keyword name , key[1] = pattern
                print key
                regex_str2.append(key[1])
        # create regex compiler for blocked keyword search
        regex_str2 = map(lambda x: x.replace("\\\\","\\"),regex_str2)
        self.blocked_keywords_re = re.compile(r'('+'|'.join(regex_str2)+')',re.IGNORECASE)
        
        # Load keywords
        with open('../twitterClass/twitterMiningClass/private/keywords.txt','r') as f:
            keywords = f.read().split('\n')
            for key in keywords:
                key = key.split(',')
                #key[0] = keyword name , key[1] = pattern
                self.keywords[key[0]] = key[1]
        # create regex compiler for keyword search
        regex_str = []
        for keys,pattern in self.keywords.iteritems():
            regex_str.append(pattern)
        regex_str = map(lambda x: x.replace("\\\\","\\"),regex_str)
        self.keywords_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
        
    def is_valid(self,tweets):
        """
            Determine if tweet(s) are valid healthcare related tweets
            
            Parameters:
            
                tweets : list of tweets with appropriate keyword matches
            
        """
        output = {}
        result = []
        for tokens in tweets:
            result.append(self.classifier.classify(preprocess.get_features(tokens)))
        for i in xrange(len(result)):
            output['valid'] = True
            output['disease'] = self.keywords_re.findall(' '.join(tweets[i]))
           
        return output
        
    def is_keyword_present(self,text):
        """
            Determine if tweet has desirable keywords
            
            Parameters:
            
                text : tokenized text from tweets
            
        """
        if self.keywords_re.search(text) and not self.blocked_keywords_re.search(text):
                print self.blocked_keywords_re.search(text)
                return True
        return False
        
    
    def is_encoded(self,text):
        """
            True if tweet has no special characters that cannot be encoded
            
            Parameters:
            
                text : raw text from tweets
            
        """
        
        try:
            str(text)
        except:
            return False
        else:
            return True