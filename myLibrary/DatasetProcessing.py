import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import compress
from tqdm import tqdm

def preProcessing(df,return_full=True,finished_games=True):
    finishedDfs=[]
    
    print("==================================\n",
          "\tBasic information\n==================================\n")
    df.shape
    df.info()
    df.describe()

    print("\nGenerating new features...")

    df["KDA"]=np.where(df["deaths"]!=0,(df["assists"]+df["kills"])/df["deaths"],df["assists"]+df["kills"])
    df["visionScore"]=df["wardsPlaced"]+df["wardsDestroyed"]
    df["improvedVisionScore"]=df["wardsPlaced"]+df["wardsDestroyed"]-df["wardsLost"]
    df["lostTopTurrets"]=df["lostTopBaseTurret"]+df["lostTopInnerTurret"]+df["lostTopOuterTurret"]
    df["destroyedTopTurrets"]=df["destroyedTopBaseTurret"]+df["destroyedTopInnerTurret"]+df["destroyedTopOuterTurret"]
    df["lostMidTurrets"]=df["lostMidBaseTurret"]+df["lostMidInnerTurret"]+df["lostMidOuterTurret"]
    df["destroyedMidTurrets"]=df["destroyedMidBaseTurret"]+df["destroyedMidInnerTurret"]+df["destroyedMidOuterTurret"]
    df["lostBotTurrets"]=df["lostBotBaseTurret"]+df["lostBotInnerTurret"]+df["lostBotOuterTurret"]
    df["destroyedBotTurrets"]=df["destroyedBotBaseTurret"]+df["destroyedBotInnerTurret"]+df["destroyedBotOuterTurret"]
    df["destroyedInhibitors"]=df["destroyedTopInhibitor"]+df["destroyedMidInhibitor"]+df["destroyedBotInhibitor"]
    df["lostInhibitors"]=df["lostTopInhibitor"]+df["lostMidInhibitor"]+df["lostBotInhibitor"]
    df["killedElemDrakes"]=df["killedFireDrake"]+df["killedWaterDrake"]+df["killedAirDrake"]+df["killedEarthDrake"]
    df["lostElemDrakes"]=df["lostFireDrake"]+df["lostWaterDrake"]+df["lostAirDrake"]+df["lostEarthDrake"]
    df["obtainedDrakeSoul"]=df["killedElemDrakes"]==4
    df["lostDrakeSoul"]=df["lostElemDrakes"]==4
    df["obtainedFireDrakeSoul"]=df["killedFireDrake"]==2
    df["obtainedWaterDrakeSoul"]=df["killedWaterDrake"]==2
    df["obtainedAirDrakeSoul"]=df["killedAirDrake"]==2
    df["obtainedEarthDrakeSoul"]=df["killedEarthDrake"]==2
    df["lostFireDrakeSoul"]=df["lostFireDrake"]==2
    df["lostWaterDrakeSoul"]=df["lostWaterDrake"]==2
    df["lostAirDrakeSoul"]=df["lostAirDrake"]==2
    df["lostEarthDrakeSoul"]=df["lostEarthDrake"]==2
    df["GameFireDrakeSoul"]=df["obtainedFireDrakeSoul"]+df["lostFireDrakeSoul"]
    df["GameWaterDrakeSoul"]=df["obtainedWaterDrakeSoul"]+df["lostWaterDrakeSoul"]
    df["GameAirDrakeSoul"]=df["obtainedAirDrakeSoul"]+df["lostAirDrakeSoul"]
    df["GameEarthDrakeSoul"]=df["obtainedEarthDrakeSoul"]+df["lostEarthDrakeSoul"]
    df["totalKilledObjectives"]=df["killedElemDrakes"]+df["killedElderDrake"]+df["killedRiftHerald"]+df["killedBaronNashor"]
    df["totalLostObjectives"]=df["lostElemDrakes"]+df["lostElderDrake"]+df["lostRiftHerald"]+df["lostBaronNashor"]
    df["totalGameKilledObjectives"]=df["totalKilledObjectives"]+df["totalLostObjectives"]
    df["totalLostTurrets"]=df["lostBotTurrets"]+df["lostMidTurrets"]+df["lostTopTurrets"]
    df["totalDestroyedTurrets"]=df["destroyedBotTurrets"]+df["destroyedMidTurrets"]+df["destroyedTopTurrets"]
    df["totalLostStructures"]=df["totalLostTurrets"]+df["lostInhibitors"]
    df["totalDestroyedStructures"]=df["totalDestroyedTurrets"]+df["destroyedInhibitors"]
    df['totalGameDestroyedStructures']=df["totalLostStructures"]+df["totalDestroyedStructures"]

    print("Done!")
    if(return_full):
        finishedDfs.append(df)
    
    if(finished_games):
        print("\nGenerating finished game data...")
        finishedGame_df=df[df.frame.eq(df.groupby('gameId').frame.transform('max'))]
        finishedGame_df=finishedGame_df.reset_index(drop=True)
        print("Done!")
        finishedDfs.append(finishedGame_df)
    
    return finishedDfs