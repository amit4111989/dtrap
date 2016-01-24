import cPickle

with open('dump/token.txt','r') as f:
    payload = f.read().split('\n')
    f.close()

tokens = [payload[0:4],payload[4:8],payload[8:12],payload[12:16]]

with open('dump/token.p','w+') as f:
    cPickle.dump(tokens,f)
    f.close()
    

    

