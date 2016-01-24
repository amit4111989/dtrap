import cPickle

with open('dump/user_list.txt','r') as f:
    payload = f.read().split('\n')
    f.close()

with open('dump/user_list.p','w+') as f:
    cPickle.dump(payload,f)
    f.close()
    
