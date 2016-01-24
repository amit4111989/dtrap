from twitterClass.twitter_main import TwitterMain
import tweepy
import datetime
import time
import cPickle

class TwitterMining(TwitterMain):
    
    tokens = ''
    ulist = ''
    authObj = ''
    settings = {}
    filenames = []
    
    def __init__(self):
        
        self.load_data()
        self.load_settings()
        self.authorize()
        super(TwitterMining,self).__init__()
        
    def load_data(self):
        """ Load private data dump """
        
        with open('../twitterClass/twitterMiningClass/private/dump/token.p','r') as f:
            self.tokens = cPickle.load(f)
            f.close()
        
        with open('../twitterClass/twitterMiningClass/private/dump/user_list.p','r') as f:
            self.ulist = cPickle.load(f)
            f.close()
            
    def load_settings(self):
        """ Load settings from text file """
        
        with open('../twitterClass/twitterMiningClass/private/settings.txt','r') as f:
            settings = f.read().split('\n')
            
        for setting in settings:
            setting = setting.split('=')
            self.settings[setting[0]] = int(setting[1])
    
    def authorize(self,token=0):
        """ 
            Instantiate auth handler object for tweepy
        
            Parameters:
            
                token : token number for auth handler
        """
        auth = tweepy.OAuthHandler(self.tokens[token][2], self.tokens[token][3])
        auth.set_access_token(self.tokens[token][0], self.tokens[token][1])
        self.authObj = tweepy.API(auth)
        
    def mine_user_timeline(self,handle):
        """
            Mine tweets from user profile given twitter handle
            
            Parameters:
                
                handle : user handle
        """
        
        obj = tweepy.Cursor(self.authObj.user_timeline, id=handle, count=self.settings['ALL_TWEETS']).items(self.settings['ALL_TWEETS'])
        return self.get_user_data(obj)
        
    def get_user_data(self,obj):
        """
            Iterate over all tweets from user timeline
            
            Parameters:
            
                obj : twitter user timeline object
        """
        
        tweets = []
        user_data = []
        filename = ''
        store_data_flag = False
        n = 0
        pending_classification = True
        samples = []
        
        for i in obj:
            
            user_data_dict = {}
            
            print i._json['user']['screen_name']
            
            if self.is_encoded(i):
                tokens = self.preprocess(i._json['text'])
            else:
                continue
            
            if n<=self.settings['INITIAL_TWEETS']:
                samples.append(i)
                if not self.is_retweet(tokens) and self.is_keyword_present(i._json['text']):
                    tweets.append(tokens)
                    print tokens
                file = open('sample.p','w+')
                n+=1
            
            else:
                cPickle.dump(samples,file)
                if pending_classification:
                    if len(tweets)==0 or len(tweets)>self.settings['MAX_TWEET_PER_KEYWORD_LIMIT']:
                        break
                    test_data = self.is_valid(tweets)
                    if not test_data['valid']:
                        break
                    else:
                        pending_classification = False
                        store_data_flag = True
                        print 'Storing data for user ',i._json['user']['screen_name']
                        #filename creation
                        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
                        filename = i._json['user']['screen_name']+'_'+st+'_'+'-'.join(test_data['disease'])
                        self.filenames.append(filename)
            
            # store user data       
            user_data_dict['text'] = tokens
            try:
                user_data_dict['lat/long'] = i.coordinates['coordinates']
            except:
                user_data_dict['lat/long'] = None
            user_data_dict['created_at'] = i.created_at
            user_data_dict['name'] = i._json['user']['screen_name']
            
            user_data.append(user_data_dict)
        
        if store_data_flag and filename:
            print user_data[len(user_data)-1]['name']
            self.store_raw_data(user_data,filename)
            #register file in the queue
            self.filenames.append(filename)
        
        return store_data_flag
    
    def get_filenames(self):
        return self.filenames
    
    def disp_tokens(self):
        print self.tokens
        
    
if __name__ == "__main__":
    
    obj = TwitterMining()
    obj.mine_user_timeline('jlsuttles')