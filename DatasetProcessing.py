import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import compress
from tqdm import tqdm

print("Loading dataframe...")
df = pd.read_csv("lol_ranked_games.csv", header=0, delimiter=',')
print("Dataframe loaded!")

print("==================================\n",
      "\t\tBasic information\n==================================\n")
df.shape
df.info()
df.describe()

print("\nGenerating new features...")

df["KDA"]=np.where(df["deaths"]!=0,(df["assists"]+df["kills"])/df["deaths"],df["assists"]+df["kills"])
df["visionScore"]=df["wardsPlaced"]+df["wardsDestroyed"]
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
df["totalLostTurrets"]=df["lostBotTurrets"]+df["lostMidTurrets"]+df["lostTopTurrets"]
df["totalDestroyedTurrets"]=df["destroyedBotTurrets"]+df["destroyedMidTurrets"]+df["destroyedTopTurrets"]
df["totalLostStructures"]=df["totalLostTurrets"]+df["lostInhibitors"]
df["totalDestroyedStructures"]=df["totalDestroyedTurrets"]+df["destroyedInhibitors"]
df['totalGameDestroyedStructures']=df["totalLostStructures"]+df["totalDestroyedStructures"]

df.describe()
print("\nGenerating expanded dataframe")
df.to_csv("ExpandedLolData.csv",index=False)
print("\nGenerating finished game data...")

finishedGame_df=df[df.frame.eq(df.groupby('gameId').frame.transform('max'))]
finishedGame_df=finishedGame_df.reset_index(drop=True)
print("\n")
finishedGame_df.info() 
finishedGame_df.to_csv("FinishedGames.csv",index=False)

objectiveAtr=["goldDiff","expDiff","champLevelDiff","kills","deaths","assists","KDA",
              "wardsPlaced","wardsDestroyed","wardsLost","visionScore","totalKilledObjectives",
              "totalLostObjectives","totalDestroyedTurrets","totalDestroyedStructures",
              "totalLostStructures","killedElemDrakes","lostElemDrakes","killedBaronNashor",
              "lostBaronNashor","lostRiftHerald"]

print("\nGenerating means, std, variances and quantiles...")

Ids=df["gameId"].unique()
for Atr in tqdm(objectiveAtr):
    STD=pd.Series([df[df["gameId"]==idx][Atr].std() for idx in Ids],name=Atr+"STD")
    VAR=pd.Series([df[df["gameId"]==idx][Atr].var() for idx in Ids],name=Atr+"VAR")
    MEAN=pd.Series([df[df["gameId"]==idx][Atr].mean() for idx in Ids],name=Atr+"MEAN")
    Q25=pd.Series([df[df["gameId"]==idx][Atr].quantile(q=0.25) for idx in Ids],name=Atr+"Q25")
    Q50=pd.Series([df[df["gameId"]==idx][Atr].quantile(q=0.5) for idx in Ids],name=Atr+"Q50")
    Q75=pd.Series([df[df["gameId"]==idx][Atr].quantile(q=0.75) for idx in Ids],name=Atr+"Q75")
    finishedGame_df=pd.concat([finishedGame_df,STD,VAR,MEAN,Q25,Q50,Q75],axis=1)

columnes=list(compress(finishedGame_df.columns,finishedGame_df.columns.str.contains('.STD$')==True))
finishedGame_df[columnes][finishedGame_df[columnes].isnull().any(axis=1)]
finishedGame_df=finishedGame_df.dropna()
print("\nSaving finished games data...")
finishedGame_df.to_csv("FinishedGamesExpanded.csv",index=False)