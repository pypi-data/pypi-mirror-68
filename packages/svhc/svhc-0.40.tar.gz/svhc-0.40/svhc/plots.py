import os
os.environ["OMP_NUM_THREADS"] = "1"
import matplotlib.pyplot as plt
import matplotlib.cm as cmap
#from metric import StandardDendrogram,OrderArray,ToMemb
import matplotlib.patches as patches
import numpy as np
import seaborn as sns
import pandas as pd
import scipy.stats as st


from collections import defaultdict,OrderedDict

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



def DendroAndCorrDist(x,validated,dendrogram,method='average',xylabel='Objects',file_w=None,color_style='Set1',nan=False,metric='pearson'):
    

    ordn = OrderArray(StandardDendrogram(ToMemb(dendrogram.keys(),x.shape[0])))
    x = x[ordn]

    rev_ornd = dict(sorted(zip(ordn,range(len(ordn)))))

    dendrogram = {tuple(sorted([rev_ornd[k] for k in K])):(np.array(sorted([rev_ornd[a] for a in dendrogram[K][0]])),
                                                   np.array(sorted([rev_ornd[a] for a in dendrogram[K][1]]))) for K in dendrogram}

    validated = [tuple(sorted([rev_ornd[k] for k in K])) for K in validated]

    if nan==False:
        if metric=='pearson':
            R = 1 - np.corrcoef(x)
        elif metric=='spearman':
            R = 1 - st.spearmanr(x.T)[0]
    else:
        R = 1. -np.array(pd.DataFrame(x.T).corr()) 
    #R = 1.-np.corrcoef(x)

    validated = sorted(validated,key=len)

    N = R.shape[0]
    K = dendrogram.keys()

    import matplotlib.patches as patches
    import colorsys
    nc  = len(validated)
    import matplotlib as mpl
    import matplotlib.cm as cm

    cnmx = sns.color_palette(color_style, nc-1)

    from collections import defaultdict
    col = defaultdict(int)
    for k in K:
        for j in range(len(validated)):
            if set(k) <= set(validated[j]):

                if tuple(validated[j])==tuple(range(N)):
                    col[tuple(k)] = 'black'
                    break

                col[tuple(k)] = cnmx[j-1]
                break


    from matplotlib import gridspec

    fig = plt.figure(figsize=(5,9))
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1.34]) 

    # the fisrt subplot
    axarr = [0,0]
    axarr[0] = plt.subplot(gs[0])
    axarr[1] = plt.subplot(gs[1], sharex = axarr[0])


    pos = defaultdict(tuple)

    for i in range(N):
        pos[(i,)] = (float(i),0)

    K = sorted(dendrogram.keys(),key=len)

    hm = []
    for k in K:
        d = tuple(sorted(dendrogram[k][0])),tuple(sorted(dendrogram[k][1]))

        c = tuple(sorted(k))
        #if not col.has_key(c):
        #    break
        pp = pos[d[0]][0],pos[d[1]][0]
        h0 = pos[d[0]][1],pos[d[1]][1]

        if method=='average':
            h = R[dendrogram[k][0]][:,dendrogram[k][1]].mean()
        elif method=='complete':
            h = R[dendrogram[k][0]][:,dendrogram[k][1]].max()
        elif method=='single':
            h = R[dendrogram[k][0]][:,dendrogram[k][1]].min()

        axarr[0].plot([pp[0],pp[0]],[h0[0],h],'-',color='k',alpha=0.5)
        axarr[0].plot([pp[1],pp[1]],[h0[1],h],'-',color='k',alpha=0.5)
        axarr[0].plot([pp[0],pp[1]],[h,h],'-',color='k',lw=1.5)
        axarr[0].plot([pp[0],pp[1]],[h,h],'-',color=col[c],lw=1.4,zorder=1000)

        hm.append(h)

        #plt.plot((pp[0]+pp[1])/2,h,'o',color=col[c],ms=4,zorder=1000)

        pos[c] = (pp[0]+pp[1])/2,h
        #print "ciao"

    axarr[0].set_yticks(np.arange(0,1.2,0.2))
    axarr[0].set_ylim([0,max(hm)+0.05])

    axarr[0].yaxis.tick_right()
    axarr[0].tick_params(labelsize=14)
    axarr[0].set_ylabel('Distance',fontsize=18)
    axarr[0].yaxis.set_label_position("right")

    if nan==False:
        R = np.corrcoef(x)
    else:
        R =  np.array(pd.DataFrame(x.T).corr()) 

    ims = axarr[1].imshow(R,vmin=-1,vmax=1,cmap=cm.RdBu_r,interpolation='nearest')


    cbar_ax = fig.add_axes([0.95, 0.133, 0.03, 0.4])
    cbr = fig.colorbar(ims, cax=cbar_ax)

    cbr.set_label('correlation',fontsize=18)
    axarr[1].set_xlabel(xylabel,fontsize=18)
    axarr[1].set_ylabel(xylabel,fontsize=18)
    axarr[1].tick_params(labelsize=14)

    axarr[1].set_ylim([0,N])

    for l in validated:
        if l == tuple(range(N)): continue

        axarr[1].add_patch(
            patches.Rectangle(
                (min(l)-0.5, min(l)-0.5),
                len(l),
                len(l),
                fill=False,
                lw=1.,
                color='green',	
                )
            )

    plt.setp(axarr[0].get_xticklabels(), visible=False)
    plt.subplots_adjust(hspace=.0)

    if file_w!=None:    
        plt.savefig(file_w+'.pdf',bbox_inches='tight')
    else:
        plt.show()


def DendroAll(x,validated,dendrogram,method='average',xylabel='Objects',file_w=None,color_style='Set1',nan=False,metric='pearson'):
    

    ordn = OrderArray(StandardDendrogram(ToMemb(dendrogram.keys(),x.shape[0])))
    x = x[ordn]

    rev_ornd = dict(sorted(zip(ordn,range(len(ordn)))))

    dendrogram = {tuple(sorted([rev_ornd[k] for k in K])):(np.array(sorted([rev_ornd[a] for a in dendrogram[K][0]])),
                                                   np.array(sorted([rev_ornd[a] for a in dendrogram[K][1]]))) for K in dendrogram}

    validated = [tuple(sorted([rev_ornd[k] for k in K])) for K in validated]

    if nan==False:
        if metric=='pearson':
            R = 1 - np.corrcoef(x)
        elif metric=='spearman':
            R = 1 - st.spearmanr(x.T)[0]
    else:
        R = 1. -np.array(pd.DataFrame(x.T).corr()) 
    #R = 1.-np.corrcoef(x)

    validated = sorted(validated,key=len)

    N = R.shape[0]
    K = dendrogram.keys()

    import matplotlib.patches as patches
    import colorsys
    nc  = len(validated)
    import matplotlib as mpl
    import matplotlib.cm as cm

    cnmx = sns.color_palette(color_style, nc-1)

    from collections import defaultdict
    col = defaultdict(int)
    
    for k in K:
        for j in range(len(validated)):
            if set(k) <= set(validated[j]):

                if tuple(validated[j])==tuple(range(N)):
                    col[tuple(k)] = 'black'
                    break

                col[tuple(k)] = 'black'
                break


    from matplotlib import gridspec

    fig = plt.figure(figsize=(5,9))
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1.34]) 

    # the fisrt subplot
    axarr = [0,0]
    axarr[0] = plt.subplot(gs[0])
    axarr[1] = plt.subplot(gs[1], sharex = axarr[0])


    pos = defaultdict(tuple)

    for i in range(N):
        pos[(i,)] = (float(i),0)

    K = sorted(dendrogram.keys(),key=len)

    hm = []
    for k in K:
        d = tuple(sorted(dendrogram[k][0])),tuple(sorted(dendrogram[k][1]))

        c = tuple(sorted(k))
        #if not col.has_key(c):
        #    break
        pp = pos[d[0]][0],pos[d[1]][0]
        h0 = pos[d[0]][1],pos[d[1]][1]

        if method=='average':
            h = R[dendrogram[k][0]][:,dendrogram[k][1]].mean()
        elif method=='complete':
            h = R[dendrogram[k][0]][:,dendrogram[k][1]].max()
        elif method=='single':
            h = R[dendrogram[k][0]][:,dendrogram[k][1]].min()

        axarr[0].plot([pp[0],pp[0]],[h0[0],h],'-',color='k',alpha=0.5)
        axarr[0].plot([pp[1],pp[1]],[h0[1],h],'-',color='k',alpha=0.5)
        axarr[0].plot([pp[0],pp[1]],[h,h],'-',color='k',lw=1.5)
        axarr[0].plot([pp[0],pp[1]],[h,h],'-',color='k',lw=1.4,zorder=1000)

        hm.append(h)

        #plt.plot((pp[0]+pp[1])/2,h,'o',color=col[c],ms=4,zorder=1000)

        pos[c] = (pp[0]+pp[1])/2,h
        #print "ciao"

    axarr[0].set_yticks(np.arange(0,1.2,0.2))
    axarr[0].set_ylim([0,max(hm)+0.05])

    axarr[0].yaxis.tick_right()
    axarr[0].tick_params(labelsize=14)
    axarr[0].set_ylabel('Distance',fontsize=18)
    axarr[0].yaxis.set_label_position("right")

    if nan==False:
        R = np.corrcoef(x)
    else:
        R =  np.array(pd.DataFrame(x.T).corr()) 

    ims = axarr[1].imshow(R,vmin=-1,vmax=1,cmap=cm.RdBu_r,interpolation='nearest')


    cbar_ax = fig.add_axes([0.95, 0.133, 0.03, 0.4])
    cbr = fig.colorbar(ims, cax=cbar_ax)

    cbr.set_label('correlation',fontsize=18)
    axarr[1].set_xlabel(xylabel,fontsize=18)
    axarr[1].set_ylabel(xylabel,fontsize=18)
    axarr[1].tick_params(labelsize=14)

    axarr[1].set_ylim([0,N])

    for l in validated:
        if l == tuple(range(N)): continue

        axarr[1].add_patch(
            patches.Rectangle(
                (min(l)-0.5, min(l)-0.5),
                len(l),
                len(l),
                fill=False,
                lw=1.,
                color='black',	
                )
            )

    plt.setp(axarr[0].get_xticklabels(), visible=False)
    plt.subplots_adjust(hspace=.0)


    if file_w!=None:    
        plt.savefig(file_w+'.pdf',bbox_inches='tight')
    else:
        plt.show()

def OnlyBox(x,validated,dendrogram,method='average',posx=[0.95, 0.285, 0.03, 0.43],xylabel='Objects',file_w=None,color_style='Set1',nan=False,metric='pearson'):
    

    ordn = OrderArray(StandardDendrogram(ToMemb(dendrogram.keys(),x.shape[0])))
    x = x[ordn]

    rev_ornd = dict(sorted(zip(ordn,range(len(ordn)))))

    dendrogram = {tuple(sorted([rev_ornd[k] for k in K])):(np.array(sorted([rev_ornd[a] for a in dendrogram[K][0]])),
                                                   np.array(sorted([rev_ornd[a] for a in dendrogram[K][1]]))) for K in dendrogram}

    validated = [tuple(sorted([rev_ornd[k] for k in K])) for K in validated]

    if nan==False:
        if metric=='pearson':
            R = 1 - np.corrcoef(x)
        elif metric=='spearman':
            R = 1 - st.spearmanr(x.T)[0]
    else:
        R = 1. -np.array(pd.DataFrame(x.T).corr()) 
    #R = 1.-np.corrcoef(x)

    validated = sorted(validated,key=len)

    N = R.shape[0]
    K = dendrogram.keys()

    import matplotlib.patches as patches
    import colorsys
    nc  = len(validated)
    import matplotlib as mpl
    import matplotlib.cm as cm

    cnmx = sns.color_palette(color_style, nc-1)

    from collections import defaultdict
    col = defaultdict(int)
    for k in K:
        for j in range(len(validated)):
            if set(k) <= set(validated[j]):

                if tuple(validated[j])==tuple(range(N)):
                    col[tuple(k)] = 'black'
                    break

                col[tuple(k)] = 'black'
                break


    from matplotlib import gridspec


    fig,arr = plt.subplots(figsize=(5,9))
    #gs = gridspec.GridSpec(1, 1, height_ratios=[1, 1.34]) 

    # the fisrt subplot
    #axarr = [0]
    #axarr[0] = plt.subplot(gs[0])
    #axarr[1] = plt.subplot(gs[1], sharex = axarr[0])


    pos = defaultdict(tuple)

    for i in range(N):
        pos[(i,)] = (float(i),0)

    K = sorted(dendrogram.keys(),key=len)

    hm = []
    for k in K:
        d = tuple(sorted(dendrogram[k][0])),tuple(sorted(dendrogram[k][1]))

        c = tuple(sorted(k))
        #if not col.has_key(c):
        #    break
        pp = pos[d[0]][0],pos[d[1]][0]
        h0 = pos[d[0]][1],pos[d[1]][1]

        if method=='average':
            h = R[dendrogram[k][0]][:,dendrogram[k][1]].mean()
        elif method=='complete':
            h = R[dendrogram[k][0]][:,dendrogram[k][1]].max()
        elif method=='single':
            h = R[dendrogram[k][0]][:,dendrogram[k][1]].min()

        #axarr[0].plot([pp[0],pp[0]],[h0[0],h],'-',color='k',alpha=0.5)
        #axarr[0].plot([pp[1],pp[1]],[h0[1],h],'-',color='k',alpha=0.5)
        #axarr[0].plot([pp[0],pp[1]],[h,h],'-',color='k',lw=1.5)
        #axarr[0].plot([pp[0],pp[1]],[h,h],'-',color='k',lw=1.4,zorder=1000)

        hm.append(h)

        #plt.plot((pp[0]+pp[1])/2,h,'o',color=col[c],ms=4,zorder=1000)

        pos[c] = (pp[0]+pp[1])/2,h
        #print "ciao"

    #axarr[0].set_yticks(np.arange(0,1.2,0.2))
    #axarr[0].set_ylim([0,max(hm)+0.05])

    #axarr[0].yaxis.tick_right()
    #axarr[0].tick_params(labelsize=14)
    #axarr[0].set_ylabel('Distance',fontsize=18)
    #axarr[0].yaxis.set_label_position("right")

    if nan==False:
        R = np.corrcoef(x)
    else:
        R =  np.array(pd.DataFrame(x.T).corr()) 

    ims = arr.imshow(R,vmin=-1,vmax=1,cmap=cm.RdBu_r,interpolation='nearest')



    cbar_ax = fig.add_axes(posx)
    cbr = fig.colorbar(ims, cax=cbar_ax)


    cbr.set_label('correlation',fontsize=18)
    arr.set_xlabel(xylabel,fontsize=18)
    arr.set_ylabel(xylabel,fontsize=18)
    arr.tick_params(labelsize=14)

    arr.set_ylim([0,N])

    for l in validated:
        if l == tuple(range(N)): continue

        arr.add_patch(
            patches.Rectangle(
                (min(l)-0.5, min(l)-0.5),
                len(l),
                len(l),
                fill=False,
                lw=1.,
                color='green',	
                )
            )

    plt.setp(arr.get_xticklabels(), visible=False)
    plt.subplots_adjust(hspace=.0)


    if file_w!=None:    
        plt.savefig(file_w+'.pdf',bbox_inches='tight')
    else:
        plt.show()

