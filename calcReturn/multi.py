import pandas as pd
import lightgbm as lgb
import math
import os
import numpy as np

from datetime import datetime as dt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def calcMulti(dfx):

    all_race_cnt = len(dfx)
    hit_race_cnt = dfx[(dfx["着順"] <= 3.0)]["着順"].count()
    back = dfx[(dfx["着順"] == 1.0)]["複勝1"]
    back = pd.concat([back,dfx[(dfx["着順"] == 2.0)]["複勝2"]])
    back = pd.concat([back,dfx[(dfx["着順"] == 3.0)]["複勝3"]])

    dfx["単勝"].to_csv("bet/bet_multi.csv",index=False)
    back.to_csv("bet/ret_multi.csv",index=False)

    back_std = back.std()
    back = back.sum()

    print(all_race_cnt)
    print("複勝　　的中率\t" + str(hit_race_cnt / all_race_cnt))
    print("複勝　　回収率\t" + str(back / all_race_cnt) + "\n")
    print("複勝　　回収率\t" + str(back_std) + "\n")

def calcMulti_even_imt(dfx,n):

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)
    hit_cnt = 0
    back = 0
    tmp_back = 0
    all_cnt = 0
    bet = 0
    backList = []
    tmp_bet100 = 0

    for race in list(dfx["レース"].drop_duplicates()):
        target = dfx[dfx["レース"] == race]

        all_cnt = all_cnt + 1
        tmp_bet = 1 / target[target["rank"]==n]["単勝"].iloc[0,]
        if np.isnan(tmp_bet):
            continue

        tmp_bet100 = tmp_bet100 + tmp_bet
        bet = bet + tmp_bet

        if len(target[(target["rank"] == n) & (target["着順"] ==1.0)]) == 1 :

            hit_cnt = hit_cnt + 1
            back = back + target["複勝1"].iloc[0,] * tmp_bet
            tmp_back = tmp_back + target["複勝1"].iloc[0,] * tmp_bet
            backList.append(target["複勝1"].iloc[0,] * tmp_bet)

        elif len(target[(target["rank"] == n) & (target["着順"] ==2.0)]) == 1 :

            hit_cnt = hit_cnt + 1
            back = back + target["複勝2"].iloc[0,] * tmp_bet
            tmp_back = tmp_back + target["複勝2"].iloc[0,] * tmp_bet
            backList.append(target["複勝2"].iloc[0,] * tmp_bet)

        elif len(target[(target["rank"] == n) & (target["着順"] ==3.0)]) == 1 :

            if ~(np.isnan(target["複勝3"].iloc[0,])):
                hit_cnt = hit_cnt + 1
                back = back + target["複勝3"].iloc[0,] * tmp_bet
                tmp_back = tmp_back + target["複勝3"].iloc[0,] * tmp_bet
                backList.append(target["複勝3"].iloc[0,] * tmp_bet)

        if all_cnt % 30 == 0:
            print("複勝1　　回収率\t" + str(tmp_back / tmp_bet100))
            tmp_back = 0
            tmp_bet100 = 0

    back_std = pd.Series(backList).std()

    print("投票数\t" + str(all_cnt))
    print("複勝1　　的中率\t" + str(hit_cnt / all_cnt))
    print("複勝1　　回収率\t" + str(back / bet) + "\n")
    print("複勝1　　標偏差\t" + str(back_std) + "\n")


