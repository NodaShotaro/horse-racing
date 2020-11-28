import pandas as pd
import lightgbm as lgb
import math
import os
import numpy as np

from datetime import datetime as dt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from calcReturn import single

def calc3renpuku(dfx):

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)

    hit_cnt = 0
    back = 0
    tmp_back = 0
    all_cnt = 0
    backList = []
    for race in list(dfx["レース"].drop_duplicates()):
        all_cnt = all_cnt + 1
        target = dfx[dfx["レース"] == race]
        if len(target[(target["rank"] == 1.0) & (target["着順"] <= 3.0)]) == 1 :
            if len(target[(target["rank"] == 2.0) & (target["着順"] <= 3.0)]) == 1 :
                if len(target[(target["rank"] == 3.0) & (target["着順"] <= 3.0)]) == 1 :
                    hit_cnt = hit_cnt + 1
                    back = back + target["三連複"].iloc[0,]
                    tmp_back = tmp_back + target["三連複"].iloc[0,]
                    backList.append(target["三連複"].iloc[0,])

        if all_cnt % 100 == 0:
            print("三連複　回収率\t" + str(tmp_back / 100))
            tmp_back = 0

    print("三連複　的中率\t" + str(hit_cnt / all_race_cnt))
    print("三連複　回収率\t" + str(back / all_race_cnt) + "\n")

    back_std = pd.Series(backList).std()
    print("三連複　回収率\t" + str(back_std) + "\n")



def calc3renpuku12_34(dfx):

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)

    hit_cnt = 0
    back = 0
    tmp_back = 0
    all_cnt = 0
    for race in list(dfx["レース"].drop_duplicates()):
        all_cnt = all_cnt + 1
        target = dfx[dfx["レース"] == race]
        if len(target[(target["rank"] == 1.0) & (target["着順"] <= 3.0)]) == 1 :
            if len(target[(target["rank"] == 2.0) & (target["着順"] <= 3.0)]) == 1 :
                if len(target[(target["rank"] == 3.0) & (target["着順"] <= 3.0)]) == 1 :
                    hit_cnt = hit_cnt + 1
                    back = back + target["三連複"].iloc[0,]
                    tmp_back = tmp_back + target["三連複"].iloc[0,]
                elif len(target[(target["rank"] == 4.0) & (target["着順"] <= 3.0)]) == 1 :
                    hit_cnt = hit_cnt + 1
                    back = back + target["三連複"].iloc[0,]
                    tmp_back = tmp_back + target["三連複"].iloc[0,]

        if all_cnt % 100 == 0:
            print("三連複：軸12　流し34　回収率\t" + str(tmp_back / 100 / 2))
            tmp_back = 0

    print("三連複　的中率\t" + str(hit_cnt / all_race_cnt))
    print("三連複　回収率\t" + str(back / all_race_cnt / 2) + "\n")

def calc3renpuku12_345(dfx):

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)

    hit_cnt = 0
    back = 0
    tmp_back = 0
    all_cnt = 0
    for race in list(dfx["レース"].drop_duplicates()):
        all_cnt = all_cnt + 1
        target = dfx[dfx["レース"] == race]
        if len(target[(target["rank"] == 1.0) & (target["着順"] <= 3.0)]) == 1 :
            if len(target[(target["rank"] == 2.0) & (target["着順"] <= 3.0)]) == 1 :
                if len(target[(target["rank"] == 3.0) & (target["着順"] <= 3.0)]) == 1 :
                    hit_cnt = hit_cnt + 1
                    back = back + target["三連複"].iloc[0,]
                    tmp_back = tmp_back + target["三連複"].iloc[0,]
                elif len(target[(target["rank"] == 4.0) & (target["着順"] <= 3.0)]) == 1 :
                    hit_cnt = hit_cnt + 1
                    back = back + target["三連複"].iloc[0,]
                    tmp_back = tmp_back + target["三連複"].iloc[0,]
                elif len(target[(target["rank"] == 5.0) & (target["着順"] <= 3.0)]) == 1 :
                    hit_cnt = hit_cnt + 1
                    back = back + target["三連複"].iloc[0,]
                    tmp_back = tmp_back + target["三連複"].iloc[0,]

        if all_cnt % 100 == 0:
            print("三連複：軸12　流し345　回収率\t" + str(tmp_back / 100 / 3))
            tmp_back = 0

    print("三連複：軸12　流し345　的中率\t" + str(hit_cnt / all_race_cnt))
    print("三連複：軸12　流し345　回収率\t" + str(back / all_race_cnt / 3) + "\n")

def calc3renpuku1_234(dfx):

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)

    hit_cnt = 0
    back = 0
    tmp_back = 0
    all_cnt = 0
    for race in list(dfx["レース"].drop_duplicates()):
        all_cnt = all_cnt + 1
        target = dfx[dfx["レース"] == race]
        if len(target[(target["rank"] == 1.0) & (target["着順"] <= 3.0)]) == 1 :
            if len(target[(target["rank"] == 2.0) & (target["着順"] <= 3.0)]) == 1 :
                if len(target[(target["rank"] == 3.0) & (target["着順"] <= 3.0)]) == 1 :
                    hit_cnt = hit_cnt + 1
                    back = back + target["三連複"].iloc[0,]
                    tmp_back = tmp_back + target["三連複"].iloc[0,]
                elif len(target[(target["rank"] == 4.0) & (target["着順"] <= 3.0)]) == 1 :
                    hit_cnt = hit_cnt + 1
                    back = back + target["三連複"].iloc[0,]
                    tmp_back = tmp_back + target["三連複"].iloc[0,]
            
            elif len(target[(target["rank"] == 3.0) & (target["着順"] <= 3.0)]) == 1 :
                if len(target[(target["rank"] == 4.0) & (target["着順"] <= 3.0)]) == 1 :
                    hit_cnt = hit_cnt + 1
                    back = back + target["三連複"].iloc[0,]
                    tmp_back = tmp_back + target["三連複"].iloc[0,]

        if all_cnt % 100 == 0:
            print("三連複：軸1　流し234　回収率\t" + str(tmp_back / 100 / 3))
            tmp_back = 0

    print("三連複：軸1　流し234　的中率\t" + str(hit_cnt / all_race_cnt))
    print("三連複：軸1　流し234　回収率\t" + str(back / all_race_cnt / 3) + "\n")


def calc3renpukuBox4(dfx):

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)

    hit_cnt = 0
    back = 0
    tmp_back = 0
    all_cnt = 0
    for race in list(dfx["レース"].drop_duplicates()):
        all_cnt = all_cnt + 1
        target = dfx[dfx["レース"] == race]
 
        if len(target[(target["rank"] <= 4.0) & (target["着順"] <= 3.0)]) == 3 :
            hit_cnt = hit_cnt + 1
            back = back + target["三連複"].iloc[0,]
            tmp_back = tmp_back + target["三連複"].iloc[0,]
 
        if all_cnt % 100 == 0:
            print("三連複：Box4　回収率\t" + str(tmp_back / 100 / 4))
            tmp_back = 0

    print("三連複：Box4　的中率\t" + str(hit_cnt / all_race_cnt))
    print("三連複：Box4　回収率\t" + str(back / all_race_cnt / 4) + "\n")

def calc3renpukuBox5(dfx):

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)

    hit_cnt = 0
    back = 0
    tmp_back = 0
    all_cnt = 0
    for race in list(dfx["レース"].drop_duplicates()):
        all_cnt = all_cnt + 1
        target = dfx[dfx["レース"] == race]
 
        if len(target[(target["rank"] <= 5.0) & (target["着順"] <= 3.0)]) == 3 :
            hit_cnt = hit_cnt + 1
            back = back + target["三連複"].iloc[0,]
            tmp_back = tmp_back + target["三連複"].iloc[0,]
 
        if all_cnt % 100 == 0:
            print("三連複：Box5　回収率\t" + str(tmp_back / 100 / 10))
            tmp_back = 0

    print("三連複：Box5　的中率\t" + str(hit_cnt / all_race_cnt))
    print("三連複：Box5　回収率\t" + str(back / all_race_cnt / 10) + "\n")

def calc3renpukuBox6(dfx):

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)

    hit_cnt = 0
    back = 0
    tmp_back = 0
    all_cnt = 0
    for race in list(dfx["レース"].drop_duplicates()):
        all_cnt = all_cnt + 1
        target = dfx[dfx["レース"] == race]
 
        if len(target[(target["rank"] <= 6.0) & (target["着順"] <= 3.0)]) == 3 :
            hit_cnt = hit_cnt + 1
            back = back + target["三連複"].iloc[0,]
            tmp_back = tmp_back + target["三連複"].iloc[0,]
 
        if all_cnt % 100 == 0:
            print("三連複：Box6　回収率\t" + str(tmp_back / 100 / 20))
            tmp_back = 0

    print("三連複：Box6　的中率\t" + str(hit_cnt / all_race_cnt))
    print("三連複：Box6　回収率\t" + str(back / all_race_cnt / 20) + "\n")


def calc3renpuku_ninki(dfx):

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)

    hit_cnt = 0
    back = 0
    tmp_back = 0
    all_cnt = 0
    backList = []
    for race in list(dfx["レース"].drop_duplicates()):

        target = dfx[dfx["レース"] == race]
        if len(target[(target["rank"] <= 2.0) & (target["人気"] == 1.0)]) == 1:
            continue

        all_cnt = all_cnt + 1

        if len(target[(target["rank"] == 1.0) & (target["着順"] <= 3.0)]) == 1 :
            if len(target[(target["rank"] == 2.0) & (target["着順"] <= 3.0)]) == 1 :
                if len(target[(target["人気"] == 1.0) & (target["着順"] <= 3.0)]) == 1 :
                    hit_cnt = hit_cnt + 1
                    back = back + target["三連複"].iloc[0,]
                    tmp_back = tmp_back + target["三連複"].iloc[0,]
                    backList.append(target["三連複"].iloc[0,])

        if all_cnt % 100 == 0:
            print("三連複　回収率\t" + str(tmp_back / 100))
            tmp_back = 0

    print(all_cnt)
    print("三連複　的中率\t" + str(hit_cnt / all_cnt))
    print("三連複　回収率\t" + str(back / all_cnt) + "\n")

    back_std = pd.Series(backList).std()
    print("三連複　回収率\t" + str(back_std) + "\n")
