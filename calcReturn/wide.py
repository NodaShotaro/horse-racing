import pandas as pd
import lightgbm as lgb
import math
import os
import numpy as np

from datetime import datetime as dt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


def calcWide(dfx):

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)
    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    backList = []
    hit_cnt = 0
    back = 0
    tmp_back = 0
    tmp_hit = 0
    all_cnt = 0
    odds = []
    for race in list(dfx["レース"].drop_duplicates()):
        all_cnt = all_cnt + 1
        target = dfx[dfx["レース"] == race]
        if len(target[(target["rank"] <= 2.0) & (target["着順"] == 1.0)]) == 1 :
            if len(target[(target["rank"] <= 2.0) & (target["着順"] == 2.0)]) == 1 :
                hit_cnt = hit_cnt + 1
                back = back + target["ワイド1-2"].iloc[0,]
                tmp_back = tmp_back + target["ワイド1-2"].iloc[0,]
                backList.append(target["ワイド1-2"].iloc[0,])
                tmp_hit = tmp_hit + 1

            elif len(target[(target["rank"] <= 2.0) & (target["着順"] == 3.0)]) == 1 :
                hit_cnt = hit_cnt + 1
                back = back + target["ワイド1-3"].iloc[0,]
                tmp_back = tmp_back + target["ワイド1-3"].iloc[0,]
                tmp_hit = tmp_hit + 1
                backList.append(target["ワイド1-3"].iloc[0,])

        elif len(target[(target["rank"] <= 2.0) & (target["着順"] == 2.0)]) == 1 :
            if len(target[(target["rank"] <= 2.0) & (target["着順"] == 3.0)]) == 1 :
                hit_cnt = hit_cnt + 1
                back = back + target["ワイド2-3"].iloc[0,]
                tmp_back = tmp_back + target["ワイド2-3"].iloc[0,]
                tmp_hit = tmp_hit + 1
                backList.append(target["ワイド2-3"].iloc[0,])

        if all_cnt % 100 == 0:
#            print("ワイド "+str(target["日付"].iloc[0,]) + " 的中率\t" + str(tmp_hit / 300))
            print("ワイド "+str(target["日付"].iloc[0,]) + " 回収率\t" + str(tmp_back / 100))
            tmp_back = 0
            tmp_hit = 0

    print("ワイド　　的中率\t" + str(hit_cnt / all_cnt))
    print("ワイド　　回収率\t" + str(back / (all_cnt))+ "\n")
    back_std = pd.Series(backList).std()
    print("ワイド　　回収率\t" + str(back_std)+ "\n")


def calcWide1_23(dfx):

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)
    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    backList = []
    hit_cnt = 0
    back = 0
    tmp_back = 0
    tmp_hit = 0
    all_cnt = 0
    odds = []
    for race in list(dfx["レース"].drop_duplicates()):
        all_cnt = all_cnt + 1
        target = dfx[dfx["レース"] == race]

        if len(target[((target["rank"] == 1.0) | (target["rank"] == 3.0)) & (target["着順"] == 1.0)]) == 1 :
            if len(target[((target["rank"] == 1.0) | (target["rank"] == 3.0)) & (target["着順"] == 2.0)]) == 1 :
                hit_cnt = hit_cnt + 1
                back = back + target["ワイド1-2"].iloc[0,]
                tmp_back = tmp_back + target["ワイド1-2"].iloc[0,]
                backList.append(target["ワイド1-2"].iloc[0,])
                tmp_hit = tmp_hit + 1

            elif len(target[((target["rank"] == 1.0) | (target["rank"] == 3.0)) & (target["着順"] == 3.0)]) == 1 :
                hit_cnt = hit_cnt + 1
                back = back + target["ワイド1-3"].iloc[0,]
                tmp_back = tmp_back + target["ワイド1-3"].iloc[0,]
                tmp_hit = tmp_hit + 1
                backList.append(target["ワイド1-3"].iloc[0,])

        elif len(target[((target["rank"] == 1.0) | (target["rank"] == 3.0)) & (target["着順"] == 2.0)]) == 1 :
            if len(target[((target["rank"] == 1.0) | (target["rank"] == 3.0)) & (target["着順"] == 3.0)]) == 1 :

                hit_cnt = hit_cnt + 1
                back = back + target["ワイド2-3"].iloc[0,]
                tmp_back = tmp_back + target["ワイド2-3"].iloc[0,]
                tmp_hit = tmp_hit + 1
                backList.append(target["ワイド2-3"].iloc[0,])

        if all_cnt % 300 == 0:
#            print("ワイド "+str(target["日付"].iloc[0,]) + " 的中率\t" + str(tmp_hit / 300))
            print("ワイド "+str(target["日付"].iloc[0,]) + " 回収率\t" + str(tmp_back / 300))
            tmp_back = 0
            tmp_hit = 0

    print("ワイド　　的中率\t" + str(hit_cnt / all_cnt))
    print("ワイド　　回収率\t" + str(back / (all_cnt))+ "\n")
    back_std = pd.Series(backList).std()
    print("ワイド　　回収率\t" + str(back_std)+ "\n")


def calcWideBox3(dfx):

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)
    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    hit_cnt = 0
    back = 0
    tmp_back = 0
    tmp_hit = 0
    all_cnt = 0
    odds = []
    for race in list(dfx["レース"].drop_duplicates()):
        all_cnt = all_cnt + 1
        target = dfx[dfx["レース"] == race]
        if len(target[(target["rank"] <= 3.0) & (target["着順"] == 1.0)]) == 1 :
            if len(target[(target["rank"] <= 3.0) & (target["着順"] == 2.0)]) == 1 :
                hit_cnt = hit_cnt + 1
                back = back + target["ワイド1-2"].iloc[0,]
                tmp_back = tmp_back + target["ワイド1-2"].iloc[0,]
                tmp_hit = tmp_hit + 1

            if len(target[(target["rank"] <= 3.0) & (target["着順"] == 3.0)]) == 1 :
                hit_cnt = hit_cnt + 1
                back = back + target["ワイド1-3"].iloc[0,]
                tmp_back = tmp_back + target["ワイド1-3"].iloc[0,]
                tmp_hit = tmp_hit + 1

        if len(target[(target["rank"] <= 3.0) & (target["着順"] == 2.0)]) == 1 :
            if len(target[(target["rank"] <= 3.0) & (target["着順"] == 3.0)]) == 1 :
                hit_cnt = hit_cnt + 1
                back = back + target["ワイド2-3"].iloc[0,]
                tmp_back = tmp_back + target["ワイド2-3"].iloc[0,]
                tmp_hit = tmp_hit + 1

        if all_cnt % 300 == 0:
#            print("ワイド "+str(target["日付"].iloc[0,]) + " 的中率\t" + str(tmp_hit / 300))
            print("ワイド "+str(target["日付"].iloc[0,]) + " 回収率\t" + str(tmp_back / 300 / 3))
            tmp_back = 0
            tmp_hit = 0

    print("ワイド　　的中率\t" + str(hit_cnt / all_cnt))
    print("ワイド　　回収率\t" + str(back / (all_cnt) / 3)+ "\n")



def calcWide_ninki(dfx):

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)
    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    backList = []
    hit_cnt = 0
    back = 0
    tmp_back = 0
    tmp_hit = 0
    all_cnt = 0
    odds = []
    for race in list(dfx["レース"].drop_duplicates()):

        target = dfx[(dfx["レース"] == race) & ((dfx["rank"]==1.0) | (dfx["人気"] == 1.0))]
        if len(target) == 1:
            continue
        all_cnt = all_cnt + 1

        if len(target[(target["着順"] == 1.0)]) == 1 :
            if len(target[(target["着順"] == 2.0)]) == 1 :
                hit_cnt = hit_cnt + 1
                back = back + target["ワイド1-2"].iloc[0,]
                tmp_back = tmp_back + target["ワイド1-2"].iloc[0,]
                backList.append(target["ワイド1-2"].iloc[0,])
                tmp_hit = tmp_hit + 1

            elif len(target[(target["着順"] == 3.0)]) == 1 :
                hit_cnt = hit_cnt + 1
                back = back + target["ワイド1-3"].iloc[0,]
                tmp_back = tmp_back + target["ワイド1-3"].iloc[0,]
                tmp_hit = tmp_hit + 1
                backList.append(target["ワイド1-3"].iloc[0,])

        elif len(target[(target["着順"] == 2.0)]) == 1 :
            if len(target[(target["着順"] == 3.0)]) == 1 :
                hit_cnt = hit_cnt + 1
                back = back + target["ワイド2-3"].iloc[0,]
                tmp_back = tmp_back + target["ワイド2-3"].iloc[0,]
                tmp_hit = tmp_hit + 1
                backList.append(target["ワイド2-3"].iloc[0,])

        if all_cnt % 100 == 0:
#            print("ワイド "+str(target["日付"].iloc[0,]) + " 的中率\t" + str(tmp_hit / 300))
            print("ワイド "+str(target["日付"].iloc[0,]) + " 回収率\t" + str(tmp_back / 100))
            tmp_back = 0
            tmp_hit = 0

    print("ワイド　　的中率\t" + str(hit_cnt / all_cnt))
    print("ワイド　　回収率\t" + str(back / (all_cnt))+ "\n")
    back_std = pd.Series(backList).std()
    print("ワイド　　回収率\t" + str(back_std)+ "\n")
