import os
os.environ["OMP_NUM_THREADS"] = "1"

import numpy as np
import fastcluster
import pandas as pd
from joblib import Parallel, delayed
import scipy.stats as st
from functools import partial
import itertools
from multiprocessing import cpu_count
import meboot

def flatten(container):
    for i in container:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i
def flatx(x):
    return tuple(flatten(x))


def dist(R,method):
    N = R.shape[0]
    d = R[np.triu_indices(N,1)]

    if method=='average':
        out = fastcluster.average(d)
    if method=='complete':
        out = fastcluster.complete(d)
    if method=='single':
        out = fastcluster.single(d)
  
    outI = out.astype(int)
    dend = {i:(i,) for i in range(N)}

    for i in range(len(outI)):
        dend[i+N] = (dend[outI[i][0]],dend[outI[i][1]])

    for i in range(N):
        dend.pop(i,None)

    dend = [(flatx(a),flatx(b)) for a,b in dend.values()]

    dend ={flatx((a,b)):(np.array(a),np.array(b)) for a,b in dend}
    
    return dend


def singPV(Rb,method):
    
    if method=='average':
        rxy = dict(map(lambda x: (x[0],Rb[x[1][0]][:,x[1][1]].mean()),LV.items()))
    if method=='complete':
        rxy = dict(map(lambda x: (x[0],Rb[x[1][0]][:,x[1][1]].max()),LV.items()))
    if method=='single':
        rxy = dict(map(lambda x: (x[0],Rb[x[1][0]][:,x[1][1]].min()),LV.items()))

    PV = list(map(lambda x:int(rxy[x[1]]<rxy[x[0]]), gen.items()))
    
    return PV



def SingleBoot(nan,method,metric,bootstrap,sel):

	if nan==False and bootstrap=='simple':
		Xb = Xg[:,sel]
	elif nan==False and bootstrap=='meboot':
		Xb = meb.bootstrap()

	if nan==False:
		if metric=='pearson':
			Rb = 1.-np.corrcoef(Xb)
		elif metric=='spearman':
			Rb = 1.-st.spearmanr(Xb.T)[0]
	else:
		Rb = 1. -Xg[sel].T.corr(method=metric).values

	return singPV(Rb,method)


def BootDist(method,Nt=1000,nan=False,ncpu=1,metric='pearson',bootstrap='simple'):

	global gen
	gen = {tuple(s):k for k in LV for s in LV[k] if len(s)>1}

	if bootstrap=='simple':
		sels = np.random.choice(range(Xg.shape[1]),replace=True,size=(Nt,Xg.shape[1]))
	elif bootstrap=='meboot':
		sels = range(Nt)
		global meb
		meb = meboot.MEBOOT(Xg)
	 
	f = partial(SingleBoot,nan,method,metric,bootstrap)

	PV = Parallel(n_jobs=ncpu, backend="threading")(delayed(f)(sel) for sel in sels)

	return sorted(zip(np.array(PV).mean(axis=0),gen.keys()))
		
def FDR(PV,alpha,N):
    p = np.array(list(zip(*PV))[0])
    thr = np.arange(1,len(PV)+1)*alpha/len(PV)

    sel = np.where(p<thr)[0]
    if len(sel)==0: 
        thr=-1.
    else:
        thr = thr[sel][-1]

    L = [range(N)]+[PV[i][1] for i in np.where(p<=thr)[0]]
    L = list(map(tuple,sorted(L,key=len,reverse=True)))

    PV = {c:p for p,c in PV}
    PV[tuple(range(N))] = np.nan
    return L,PV

def Bootstrap_PV(LV,X,Nt):
    gen = {tuple(s):k for k in LV for s in LV[k] if len(s)>1}

    sels = sd.choice(range(X.shape[1]),replace=False,size=(Nt,X.shape[1]))

    PV = Pvalues(X,sels,LV,gen)
    return PV

def Analytic_PV(r,n):
    R = 1-r
    gen = {tuple(s):k for k in LV for s in LV[k] if len(s)>1}

    sd = np.vectorize(lambda x: (1./n)*(1-x**2)**2)
    COV = lambda i,j: (0.5/n)*(((R[i[0],j[0]]-R[i[0],i[1]]*R[j[0],i[1]])*(R[i[1],j[1]]-R[i[1],j[0]]*R[j[0],j[1]]))+((R[i[0],j[1]]-R[i[0],j[0]]*R[j[0],j[1]])*(R[i[1],j[0]]-R[i[1],i[0]]*R[i[0],j[0]]))+((R[i[0],j[0]]-R[i[0],j[1]]*R[j[1],j[0]])*(R[i[1],j[1]]-R[i[1],i[0]]*R[i[0],j[1]]))+((R[i[0],j[1]]-R[i[0],i[1]]*R[i[1],j[1]])*(R[i[1],j[0]]-R[i[1],j[1]]*R[j[1],j[0]])))
    PV = []
    for h,(son,fat) in enumerate(gen.items()):


        a_s,b_s = LV[son]
        a_f,b_f = LV[fat]

        m = R[a_s][:,b_s].mean()-R[a_f][:,b_f].mean()

        ss = sd(R[a_s][:,b_s])
        sf = sd(R[a_f][:,b_f])

        elm_f = list(itertools.product(a_f, b_f))
        elm_s = list(itertools.product(a_s, b_s))

        ns = 1./np.size(ss)
        nf = 1./np.size(sf)

        cf = (nf**2)*2*sum(COV(elm_f[i],elm_f[j]) for i in range(len(elm_f)) for j in range(i))
        cs = (ns**2)*2*sum(COV(elm_s[i],elm_s[j]) for i in range(len(elm_s)) for j in range(i))
        cmix = -2*(ns*nf)*sum(COV(elm_f[i],elm_s[j]) for i in range(len(elm_f)) for j in range(len(elm_s)))

        x = (ns**2)*ss.sum()+(nf**2)*sf.sum()+cf+cs+cmix

        s = np.sqrt(x)

        PV.append((st.norm.cdf(0,m,s),son))

    return PV

def Find_ValidatedCluster(X,Nt=1000,alpha=0.05,ncpu=cpu_count(),dendrogram=None,method='average',metric='pearson',bootstrap='simple'):

	global sd
	sd = np.random.RandomState(0)

	nan = np.isnan(X).any()
	if nan==True and bootstrap=='meboot':
		raise Exception('meeboot does not accept nan')

	if nan==False:
		if metric=='pearson':
			R = 1. - np.corrcoef(X)
		elif metric=='spearman':
			R = 1. -st.spearmanr(X.T)[0]
	else:
		X = pd.DataFrame(X)
		R = 1. -X.T.corr(method=metric).values

	global Xg
	Xg = X

	global LV
	if dendrogram==None:
		LV = dist(R,method)
	else:
		LV = dendrogram


	if Nt==0:
		PV = Analytic_PV(R,X.shape[1])
	else:
		PV = BootDist(method,Nt,nan,ncpu,metric,bootstrap)

	PV = [(p,tuple(sorted(k))) for p,k in PV]

	L,PV = FDR(PV,alpha,X.shape[0])

	return {'validated':L,'pvalues':PV,'dendrogram':LV}

