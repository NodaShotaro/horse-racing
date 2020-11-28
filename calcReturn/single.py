import pandas as pd
import lightgbm as lgb
import math
import os
import numpy as np

from datetime import datetime as dt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def calcAll(df):

    df["購入額"] = 1 / df["単勝"]
    pay = df["購入額"].sum()
    hit_race_cnt = df[(df["着順"] == 1.0)]["着順"].count()
    odds10_cnt = df[(df["単勝"] >= 10)]["着順"].count()
    odds30_cnt = df[(df["単勝"] >= 30)]["着順"].count()
    odds100_cnt = df[(df["単勝"] >= 100)]["着順"].count()

    df["回収30"] = df["回収"]
    df.loc[df["単勝"]>30,"回収30"] = 0
    df["回収"].to_csv("bet.csv",index=False,sep="\t")

    print("的中率　 ：\t"+ str(hit_race_cnt / len(df)))
    print("ノーマル ：\t"+ str(df["回収"].mean()))
    print("逆数買い ：\t"+ str(hit_race_cnt / pay))
    print("合計件数 ：\t"+ str(df["回収"].count()))
    print("10以上数 ：\t"+ str(odds10_cnt))
    print("30以上数 ：\t"+ str(odds30_cnt))
    print("100以上数：\t"+ str(odds100_cnt))

def calc(df):

    df["購入額"] = 1 / df["単勝"]
    pay = df["購入額"].sum()
    hit_race_cnt = df[(df["着順"] == 1.0)]["着順"].count()
    return hit_race_cnt / pay

def calcSingle(dfx):

    dfx["購入額"] = 1 / dfx["単勝"]
    pay = dfx[(dfx["rank"] == 1.0)]["購入額"].sum()

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]
    hit_race_cnt = dfx[(dfx["rank"] == 1.0) & (dfx["着順"] == 1.0)]["着順"].count()

    back = dfx[(dfx["rank"] == 1.0) & (dfx["着順"] == 1.0)]["単勝"].sum()
    dfx[(dfx["rank"] == 1.0) & (dfx["着順"] == 1.0)]["単勝"].to_csv("bet/ret.csv",index=False)
    dfx[(dfx["rank"] == 1.0)]["単勝"].to_csv("bet/bet.csv",index=False)
    back_std = dfx[(dfx["rank"] == 1.0) & (dfx["着順"] == 1.0)]["単勝"].std()

    print("レース数\t" + str(all_race_cnt))
    print("単勝1　的中率\t" + str(hit_race_cnt / all_race_cnt))
    print("単勝1　回収率\t" + str(back / all_race_cnt))
    print("単勝1　均等買い\t" + str(hit_race_cnt / pay))
    print("単勝1　標偏差\t" + str(back_std) + "\n")



    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]
    hit_race_cnt = dfx[(dfx["rank"] == 2.0) & (dfx["着順"] == 1.0)]["着順"].count()
    back = dfx[(dfx["rank"] == 2.0) & (dfx["着順"] == 1.0)]["単勝"].sum()
    back_std = dfx[(dfx["rank"] == 2.0) & (dfx["着順"] == 1.0)]["単勝"].std()
    pay = dfx[(dfx["rank"] == 2.0)]["購入額"].sum()

    print("レース数\t" + str(all_race_cnt))
    print("単勝2　的中率\t" + str(hit_race_cnt / all_race_cnt))
    print("単勝2　回収率\t" + str(back / all_race_cnt))
    print("単勝2　均等買い\t" + str(hit_race_cnt / pay))
    print("単勝2　標偏差\t" + str(back_std) + "\n")

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]
    hit_race_cnt = dfx[(dfx["rank"] == 3.0) & (dfx["着順"] == 1.0)]["着順"].count()
    back = dfx[(dfx["rank"] == 3.0) & (dfx["着順"] == 1.0)]["単勝"].sum()
    back_std = dfx[(dfx["rank"] == 3.0) & (dfx["着順"] == 1.0)]["単勝"].std()
    pay = dfx[(dfx["rank"] == 3.0)]["購入額"].sum()

    print("レース数\t" + str(all_race_cnt))
    print("単勝3　　的中率\t" + str(hit_race_cnt / all_race_cnt))
    print("単勝3　　回収率\t" + str(back / all_race_cnt))
    print("単勝3　均等買い\t" + str(hit_race_cnt / pay))
    print("単勝3　　標偏差\t" + str(back_std) + "\n")