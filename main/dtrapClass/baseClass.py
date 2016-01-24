import sys
import os
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import cPickle
import Queue
import datetime
import time
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtrap.settings.local")
#from main.models import Main


class Dtrap(object):
    
    que = ''
    rules_data ={}
    profiling_data = {}
    
    
    def __init__(self):
        self.setup()
    
    def db_store(self):
        pass
    
    def setup(self):
        self.que = Queue.Queue()
    
    def store_raw_data(self,data,filename):
        with open('../data/'+filename+'.p','w+') as f:
            cPickle.dump(data,f)
            
    def register_job(self,filename):
        self.que.put(filename)
        
    def fetch_job(self):
        if not self.que.empty():
            return self.que.get()
        else:
            return False
            
    def store_raw_analysis_data(self,data,profile=False):
        if not profile:
            self.rules_data.update(data)
        else:
            self.profiling_data.update(data)
            
    def dump_analysis_data(self):
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
        with open('../data_analysis/analysis_'+st+'.p','w+') as f:
            data = [self.rules_data,self.profiling_data]
            cPickle.dump(data,f)
        self.initialize()
        
    def initialize(self):
        self.rules_data = {}
        self.profiling_data = {}
