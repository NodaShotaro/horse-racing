import pandas as pd
import lightgbm as lgb
import math
import os
import numpy as np

from datetime import datetime as dt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def calcSingle(dfx):

    dfx["購入額"] = 1 / dfx["単勝"]
    pay = dfx[(dfx["rank"] == 1.0)]["購入額"].sum()

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]
    hit_race_cnt = dfx[(dfx["rank"] == 1.0) & (dfx["着順"] == 1.0)]["着順"].count()

    back = dfx[(dfx["rank"] == 1.0) & (dfx["着順"] == 1.0)]["単勝"].sum()
    back_std = dfx[(dfx["rank"] == 1.0) & (dfx["着順"] == 1.0)]["単勝"].std()

    print("レース数\t" + str(all_race_cnt))
    print("単勝1　的中率\t" + str(hit_race_cnt / all_race_cnt))
    print("単勝1　回収率\t" + str(back / all_race_cnt))
    print("単勝1　均等買い\t" + str(hit_race_cnt / pay) + "\n")
    print("単勝1　標偏差\t" + str(back_std) + "\n")



    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]
    hit_race_cnt = dfx[(dfx["rank"] == 2.0) & (dfx["着順"] == 1.0)]["着順"].count()
    back = dfx[(dfx["rank"] == 2.0) & (dfx["着順"] == 1.0)]["単勝"].sum()
    back_std = dfx[(dfx["rank"] == 2.0) & (dfx["着順"] == 1.0)]["単勝"].std()
    pay = dfx[(dfx["rank"] == 2.0)]["購入額"].sum()

    print("レース数\t" + str(all_race_cnt))
    print("単勝2　的中率\t" + str(hit_race_cnt / all_race_cnt))
    print("単勝2　回収率\t" + str(back / all_race_cnt))
    print("単勝2　均等買い\t" + str(hit_race_cnt / pay) + "\n")
    print("単勝2　標偏差\t" + str(back_std) + "\n")

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]
    hit_race_cnt = dfx[(dfx["rank"] == 3.0) & (dfx["着順"] == 1.0)]["着順"].count()
    back = dfx[(dfx["rank"] == 3.0) & (dfx["着順"] == 1.0)]["単勝"].sum()
    back_std = dfx[(dfx["rank"] == 3.0) & (dfx["着順"] == 1.0)]["単勝"].std()
    pay = dfx[(dfx["rank"] == 3.0)]["購入額"].sum()

    print("レース数\t" + str(all_race_cnt))
    print("単勝3　　的中率\t" + str(hit_race_cnt / all_race_cnt))
    print("単勝3　　回収率\t" + str(back / all_race_cnt) + "\n")
    print("単勝3　均等買い\t" + str(hit_race_cnt / pay) + "\n")
    print("単勝3　　標偏差\t" + str(back_std) + "\n")

def calcSingle_simple(dfx):


    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]
    hit_race_cnt = dfx[(dfx["rank"] == 1.0) & (dfx["着順"] == 1.0)]["着順"].count()
    back = dfx[(dfx["rank"] == 1.0) & (dfx["着順"] == 1.0)]["単勝"].sum()

    print("レース数\t" + str(all_race_cnt))
    print("単勝1　的中率\t" + str(hit_race_cnt / all_race_cnt))
    print("単勝1　回収率\t" + str(back / all_race_cnt))

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]
    hit_race_cnt = dfx[(dfx["rank"] == 2.0) & (dfx["着順"] == 1.0)]["着順"].count()
    back = dfx[(dfx["rank"] == 2.0) & (dfx["着順"] == 1.0)]["単勝"].sum()

    print("単勝2　的中率\t" + str(hit_race_cnt / all_race_cnt))
    print("単勝2　回収率\t" + str(back / all_race_cnt))

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]
    hit_race_cnt = dfx[(dfx["rank"] == 3.0) & (dfx["着順"] == 1.0)]["着順"].count()
    back = dfx[(dfx["rank"] == 3.0) & (dfx["着順"] == 1.0)]["単勝"].sum()

    print("単勝3　　的中率\t" + str(hit_race_cnt / all_race_cnt))
    print("単勝3　　回収率\t" + str(back / all_race_cnt) + "\n")

