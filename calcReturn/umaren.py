import pandas as pd
import lightgbm as lgb
import math
import os
import numpy as np

from datetime import datetime as dt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def isBothOver10(target,rank1,rank2):
    odds1 = target[target["rank"]==rank1]["単勝"].iloc[0,]
    odds2 = target[target["rank"]==rank2]["単勝"].iloc[0,]

    if (odds1 > 5) & (odds2 > 5):
        return True
    else:
        return False

def calcScore(target,rank1,rank2):
    score1 = target[target["rank"]==rank1]["勝_p_mean"].iloc[0,]
    score2 = target[target["rank"]==rank2]["勝_p_mean"].iloc[0,]
    return score1+score2

def calcRet(target,rank1,rank2):

    if len(target[(target["rank"] == rank1) & (target["着順"] <= 2.0)]) == 1 :
        if len(target[(target["rank"] == rank2) & (target["着順"] <= 2.0)]) == 1 :
            return target["馬連"].iloc[0,]
    return 0
    
def calcUmaren(dfx):

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)
    hit_cnt = 0
    back = 0
    votes = 0
    backList = pd.DataFrame()

    score_border = 2.4

    for race in list(dfx["レース"].drop_duplicates()):
        target = dfx[dfx["レース"] == race]

        for i in range(1,len(target)+1):
            for j in range(i+1,len(target)+1):
                tmp_score = calcScore(target,i,j)
                if isBothOver10(target,i,j):
                    continue

                if tmp_score >= score_border:
                    votes = votes+1
                    tmp_back = calcRet(target,i,j)
                    if tmp_back > 0:
                        print(race + "\t" + str(tmp_back))
                        back = back+tmp_back               
                        hit_cnt = hit_cnt + 1
                        backList.append({
                            "レース" : race,
                            "単勝1" : target[target["rank"]==i]["単勝"].iloc[0,], 
                            "単勝2" : target[target["rank"]==j]["単勝"].iloc[0,], 
                            "score1" : target[target["rank"]==i]["勝_p_mean"].iloc[0,], 
                            "score2" : target[target["rank"]==j]["勝_p_mean"].iloc[0,], 
                            "馬連" : target["馬連"].iloc[0,]
                        },ignore_index=True)
                else:
                    break

    print("馬連　　投票数\t" + str(votes))
    print("馬連　　的中率\t" + str(hit_cnt / votes))
    print("馬連　　回収率\t" + str(back / votes) + "\n")
    backList.to_csv("bet.csv",index=False)
