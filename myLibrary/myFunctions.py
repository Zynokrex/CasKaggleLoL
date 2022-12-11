import matplotlib.pyplot as plt
import numpy as np

def doublePieWonLost(df, col1, col2, title, labels, figsize=(10,10), size=0.3):
    resultsToPlot={}
    Results=df[col2].unique()

    for res in Results:
        dS_true=df[(df[col1]==1) & (df[col2]==res)][col1].count()
        dS_false=df[(df[col1]==0) & (df[col2]==res)][col1].count()
        resultsToPlot[res]=[dS_true,dS_false]

    fig, ax = plt.subplots(figsize=figsize)
    
    vals=np.array(list(resultsToPlot.values()))

    cmap = plt.colormaps["tab20c"]
    outer_colors = cmap(np.arange(6)*4)
    inner_colors = cmap([2,3,6,7,9,10,13,14,17,18,21,22])
    
    if(len(labels)!=len(resultsToPlot.keys())):
        print("Error: longitud de labels diferent a de les x\n",
                "S'assignaran valors automatics")
        labels=list(resultsToPlot.keys())
    
    ax.pie(vals.sum(axis=1),radius=1, colors=outer_colors,
           wedgeprops=dict(width=size, edgecolor='w'),
          labels=labels,autopct='%1.1f%%',
          pctdistance=0.8)

    ax.pie(vals.flatten(), radius=1-size, colors=inner_colors,
           wedgeprops=dict(width=size, edgecolor='w'),autopct='%1.1f%%',
          pctdistance=1-size)

    ax.legend(labels,loc='upper left')
    ax.set(aspect="equal", title=title)
    plt.show()
    
def expAndGoldProgress(df,idx,save=False):
    grafic=(df[df["gameId"]==idx]["frame"],
            df[df["gameId"]==idx]["goldDiff"],
            df[df["gameId"]==idx]["expDiff"])
    plt.figure(figsize=(15,15))
    plt.scatter(grafic[0],grafic[1])
    plt.plot(grafic[0],grafic[1])
    plt.scatter(grafic[0],grafic[2],color='red')
    plt.plot(grafic[0],grafic[2],color='red')
    plt.legend(labels=["frame","gold","frame","xp"],prop={'size': 15})
    if(save):
        plt.savefig(str(idx)+'.png')
        print("Image saved")