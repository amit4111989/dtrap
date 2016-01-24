from baseClass import Dtrap
import time
import cPickle
from analysisProfilingClass.analysis_profiling import AnalysisProfiling
from analysisRulesClass.analysis_rules import AnalysisRules
from twitterClass.twitterMiningClass.twitter_mining import TwitterMining
import django
django.setup()

class AnalysisMain(Dtrap):
    
    busy = False
    profilingInstance='',
    rulesInstance='',
    current_user_data = ''
        
    def __init__(self,profilingInstance,rulesInstance):
        self.profilingInstance = profilingInstance
        self.rulesInstance = rulesInstance
        super(AnalysisMain,self).__init__()
        
    def start_analysis(self,filename):
        self.busy = True
        inp = self.get_user_data(filename)
        dis = filename.split('_')
        dis = dis[len(dis)-1].split('.')[0]
        disease = dis.split('-')
        self.profilingInstance.profile(inp,disease)
        rules_data = self.rulesInstance.extract_rules_data(inp['tweets'],disease)
        super(self.__class__,self).store_raw_analysis_data(rules_data)
        self.current_user_data = ''
        self.busy = False
        super(self.__class__,self).dump_analysis_data()
        
    def get_user_data(self,filename):
        data = ''
        with open('../data/'+filename,'r') as f:
            data = cPickle.load(f)
        self.current_user_data = data
        return self.seperate_data()
    
    def seperate_data(self):
        output = {}
        retweets = []
        tweets = []
        for data in self.current_user_data:
            if data['text'][0]=='rt':
                retweets.append(data)
            else:
                tweets.append(data)
        output['retweets'] = retweets
        output['tweets'] = tweets
        return output
    
    def analyze_rules(self):
        self.rulesInstance.generate_rules(self.rules_data)

        
if __name__=="__main__":
    
    s = 0.1
    c = 0.5
    
    mining = TwitterMining()
    #Get user list
    
    with open('../ulist/users_sfo.txt','r') as f:
        users = f.read().split('\n')
    
    for user in users:
        mining.mine_user_timeline(user)
    
    filenames = mining.get_filenames()
    for files in filenames:
        profileObj = AnalysisProfiling()
        rulesObj = AnalysisRules(s,c)
        obj = AnalysisMain(profileObj,rulesObj)
        obj.start_analysis(files+'.p')
    
    