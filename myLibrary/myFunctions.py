import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn.metrics as metrics
import sklearn.model_selection as model_selection
import time
from sklearn.inspection import permutation_importance

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
        
def oneFeatureClassification(X_train,Y_train,X_test,Y_test,model,show_numeric_results=False):
    features = X_train.columns
    Roc, F1 = [], []
    features = features.tolist()

    for idx, feature in enumerate(features):
        classf=model.fit(np.array(X_train[feature]).reshape(-1,1), Y_train)
        preds = classf.predict(np.array(X_test[feature]).reshape(-1,1))
        try:
            y_pred_proba = classf.decision_function(np.array(X_test[feature]).reshape(-1,1))
        except AttributeError:
            y_pred_proba = classf.predict_proba(np.array(X_test[feature]).reshape(-1,1))[:,1]
        else:
            pass
        roc=metrics.roc_auc_score(Y_test, y_pred_proba)    
        f1 = metrics.f1_score(Y_test, preds, average='weighted')
        Roc.append(roc)
        F1.append(f1)
        if(show_numeric_results):
            print(f"{feature} - ROC: {roc:.3f}; F1: {f1:.3f};")

    roc = np.array(Roc)
    f1 = np.array(F1)
    plt.figure(figsize=(30,10)) 
    plt.bar(np.arange(len(features)) - 0.1, roc, 0.2, label = 'roc')
    plt.bar(np.arange(len(features)) + 0.1, f1, 0.2, label = 'f1')
    plt.axhline(y=1,color='r',linestyle='--')
    plt.title("diferent metrics for each individual feature classification")
    plt.ylabel("metrics values")
    plt.xlabel('feature name')
    plt.xticks(range(0,len(features)),features,rotation=90)
    plt.legend()
    plt.show()

def fullModelClassification(model,X_train,Y_train,X_test,Y_test,
                            save_results=False):
    print("Model: "+type(model).__name__)
    
    #Model training
    start=time.time()
    model.fit(X_train,Y_train)
    end=time.time()
    print("Training time is: ",end-start,"s")
    
    #Model testing
    prediction_rm=model.predict(X_test)
    y_pred = model_selection.cross_val_predict(model,X_test,Y_test,cv=10)
    sns.heatmap(metrics.confusion_matrix(Y_test,y_pred),
                annot=True,
                fmt='3.0f',
                cmap="viridis",
               )
    plt.title('Confusion_matrix', y=1.05, size=15)
    
    try:
        y_pred_proba = model_selection.cross_val_predict(model,
                                                         X_test,
                                                         Y_test,
                                                         method='decision_function')
    except AttributeError:
        y_pred_proba = model_selection.cross_val_predict(model,
                                                         X_test,
                                                         Y_test,
                                                         method='predict_proba')[:,1]         
    else:
        pass

    score=model.score(X_test,Y_test)
    roc=metrics.roc_auc_score(Y_test, y_pred_proba)
    f1 = metrics.f1_score(Y_test, y_pred, average='weighted')
    accuracy=metrics.accuracy_score(Y_test, y_pred)
    precision=metrics.precision_score(Y_test, y_pred, average='weighted')
    print("Base sklearn score is: ",score)
    print("ROC score is: ", roc)
    print("F1 score is:", f1)
    print("Accuracy score is:", accuracy)
    print("Precision score is:", precision)
    metrics.RocCurveDisplay.from_estimator(model,X_test,Y_test)
    metrics.PrecisionRecallDisplay.from_estimator(model,X_test,Y_test)
    if(save_results):
        return(type(model).__name__,
               [model,end-start,{"score":score,
                                 "ROC":roc,
                                 "F1":f1,
                                 "Accuracy":accuracy,
                                 "Precision":precision}],
              )
    
def featureImportance(X_train,Y_train,model,feature_names,figsize=(100,30)):
    result=permutation_importance(model, X_train,
                                  Y_train,n_repeats=5,random_state=2,n_jobs=2)
    importances=pd.Series(result.importances_mean,
                             index=feature_names)
    fig, ax = plt.subplots(figsize=figsize)
    importances.plot.bar(yerr=result.importances_std, ax=ax)
    ax.set_title("Feature importances using permutation on full model")
    ax.set_ylabel("Mean accuracy decrease")
    fig.tight_layout()
    plt.show()
    