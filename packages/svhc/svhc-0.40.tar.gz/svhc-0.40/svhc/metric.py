import os
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
import scipy.special as ss
from collections import defaultdict,OrderedDict
import matplotlib.pyplot as plt
import sys
import pandas as pd

def ToMemb(nod,N):
    h = np.array([-1]*N)

    nod = sorted(nod,key=lambda x:len(x),reverse=True)
    Hn = []
    sel = {}
    while True:
        c = 0
        for i in range(len(nod)):
            if i in sel: continue
            if not all(h[np.array(nod[i])]==-1): continue

            h[np.array(nod[i])]=c
            sel[i] = None
            c+=1

        h[h==-1] = np.arange(h.max()+1,(h==-1).sum()+h.max()+1)
        Hn.append(h)
        h = np.array([-1]*N)
        if len(sel)==len(nod):
            break

    Hn.append(np.arange(N))    
    return Hn

    
def StandardDendrogram(H):
	h = sorted(list(zip(*H)))
	h = list(map(list,h))

	for j in range(len(h[0])-1):
		k = OrderedDict.fromkeys(list(zip(*h))[j]).keys()
		k = dict(zip(k,range(len(k))))

		for i in range(len(h)):
			h[i][j] = k[h[i][j]]

	j = len(h[0])-1

	k = OrderedDict.fromkeys(list(zip(*h))[j]).keys()
	k = dict(zip(k,range(len(k))))

	h = sorted(h,key=lambda x:x[-1])

	for i in range(len(h)):
			h[i][j] = k[h[i][j]]
			
	h = list(map(np.array,zip(*h)))
	return h

def OrderArray(H):
    return np.array( list(zip(*sorted(zip(H[-1],range(len(H[0]))))))[1] )


def FiltMatrix(R,clust,method='average'):
	N = R.shape[0]

	Rv = np.identity(N)

	Done = ~np.identity(N).astype(bool)

	C = map(np.array,sorted(clust,key=len))

	for c in C:
		one = np.zeros(N)

		one[c] = 1
		if method=='average':
			Rv[np.where(np.outer(one,one)*Done)] = R[np.where(np.outer(one,one)*Done)].mean()
		elif method=='complete':
			 Rv[np.where(np.outer(one,one)*Done)] = R[np.where(np.outer(one,one)*Done)].min()
		elif method=='single':
			 Rv[np.where(np.outer(one,one)*Done)] = R[np.where(np.outer(one,one)*Done)].max()


		Done[np.where(np.outer(one,one)*Done)] = False

	return Rv
