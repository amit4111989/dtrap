from baseClass import Dtrap
import apriori

class AnalysisRules(Dtrap):
    
    minSC = ''
    minCON = ''
    
    def __init__(self,minSupport,minConfidence):
        
        self.minSC = minSupport
        self.minCON =minConfidence
        pass
    
    def generate_rules(self,data):
        
        results = apriori.run(data,self.minSC,self.minCON)
        #self.db_store(results,type='rules')
    
    def extract_rules_data(self,data,disease):
        lines = {}
        file = open('../public_data/rules_data.csv','w')
        for rows in data:
            if rows['lat/long']:
                coords = rows['lat/long']
                for dis in disease:
                    file.write(str(dis)+','+str(coords))
                    file.write('\n')
                    file.write(str(dis)+','+str(coords))
                    file.write('\n')
                    lines.update({dis:str(coords)})
                    lines.update({dis:str(coords)})
        file.close()
        return lines
        

if __name__=="__main__":
    
    with open("INTEGRATED-DATASET.csv",'r') as f:
        payload = f.read().split('\n')
    data = []
    for lines in payload:
        lines = lines.strip().rstrip(',') 
        print lines
        data.append(lines.split(','))
    
    obj = AnalysisRules(0.1,0.5)
    obj.generate_rules(data)
    
    
    
    
    