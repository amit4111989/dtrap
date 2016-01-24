from baseClass import Dtrap

class AnalysisProfiling(Dtrap):
    
    profiling_keywords = []
    
    def __init__(self):
        
        self.load_profiling_keywords()
        
    def load_profiling_keywords(self):
        
        payload = ''
        with open('analysisProfilingClass/profiling_keywords.txt','r') as f:
            
            payload = f.read().split('\n')
        
        for profile in payload:
            profiles = {}
            name = profile.split(':')[0]
            keywords = profile.split(':')[1]
            keywords = keywords.split('#')
            key_array = []
            for keys in keywords:
                keys = keys.split(',')
                key_array.append([keys[0],keys[1]])   
            profiles[name] = key_array
            self.profiling_keywords.append(profiles)
    
    def profile(self,data,disease):
        
        profile_scores = {}
        output = {}
        
        for lines in data['tweets']:
                count=0.0
                for profiles in self.profiling_keywords:
                    
                    for k,v in profiles.iteritems():
                        for keys in v:
                            if keys[0] in lines['text']:
                                count= float(keys[1])+count
                        
                        profile_scores[k]=count
                                
        
        
        print profile_scores
        file = open('../public_data/profile_data.csv','w')
        for j in disease:
                
                public_data = {}
                profiles = []
                for k,v in profile_scores.iteritems():
                        profiles.append(str(k)+'#'+str(v))
                public_data[j] = profiles
                file.write(str(j)+','+','.join(profiles))
                file.write('\n')
                output.update({j:profile_scores})
        file.close()
        print output
        #print output
        super(self.__class__,self).store_raw_analysis_data(output,profile=True)
    
        
        