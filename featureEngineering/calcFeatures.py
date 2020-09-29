import pandas as pd
import numpy as np

def join(df_h,df_r):

       df_h.drop(['天気','枠番', '馬番', 'オッズ', '人気','不利',"出遅れ","ﾀｲﾑ指数","距離カテゴリ",
              '着順', '騎手', '斤量', '距離', '馬場', 'タイム', '通過', '上り', '馬体重',
              '賞金','コースの種類', 'ペース(前半)', 'ペース(後半)',
              '馬体重の差分'],axis=1,inplace=True)

       df_r.drop(["レース名"],axis=1,inplace=True)
       df_r["レース"] = df_r["日付"].astype("str") + "-" + df_r["R"].astype("str") + "-" + df_r["開催"]

       print(len(df_r))
       print("馬名")
       dx = pd.merge(df_r,df_h,on=["日付","開催","R","馬名"])
       print(len(dx))

       return dx

def makeCrossCategory(df):

    # コース系列
    df["コース*距離"] = df["コースの種類"] + df["距離"].astype(str)
    df["コース*馬場"] = df["コースの種類"] + df["馬場"].astype(str)
    df["コース*枠番"] = df["コースの種類"] + df["枠番"].astype(str)

    return df

def calc(df):

    ## 前処理
    df["日付"] = pd.to_datetime(df["日付"])
    df["生年月日"] = pd.to_datetime(df["生年月日"],format="%Y年%m月%d日")
    df["距離"] = df["距離"].astype("int")

    df = makeCrossCategory(df)
    df["=1前コースの種類"] = df["コースの種類"] == df["1前コースの種類"]
    df["=1前レース条件"] = df["レース条件"] == df["1前レース条件"]

    df["乗替り"] = df["騎手"] == df["1前騎手"]
    df["馬番奇数"] = df["馬番"] % 2 == 1

    df["2連続_距離カテゴリ"] = (df["距離"] == df["1前距離"]) & (df["コースの種類"]==df["1前コースの種類"])
    df["3連続_距離カテゴリ"] = (df["距離"] == df["1前距離"]) & (df["コースの種類"]==df["1前コースの種類"]) & (df["距離"] == df["2前距離"]) & (df["コースの種類"]==df["2前コースの種類"])

    # 馬体重の系列
    df["距離/1前距離"] = (df["距離"] / df["1前距離"])
    df["馬体重の差分/馬体重"] = df["馬体重の差分"] / df["馬体重"]
    df["距離/1前距離 * 馬体重の差分/馬体重"] = df["距離/1前距離"] * df["馬体重の差分/馬体重"]

    df["2前との馬体重の差分"] = df["2前馬体重"] - df["馬体重"]
    df["3前との馬体重の差分"] = df["3前馬体重"] - df["馬体重"]

    df["馬体重/2前馬体重"] = df["馬体重"] / df["2前馬体重"]
    df["馬体重/3前馬体重"] = df["馬体重"] / df["3前馬体重"]
    df["斤量/馬体重"] = df["斤量"] / df["馬体重"]
    df["斤量差分"] = df["斤量"] - df["1前斤量"]

    df["馬体重+斤量の差分"] = df["馬体重の差分"] + df["斤量差分"]
    df["馬体重+斤量の割合"] = (df["馬体重の差分"] + df["斤量差分"]) / (df["馬体重"] + df["斤量"])

    df["馬体重 * 距離"] = df["距離"] * df["馬体重"]
    df["斤量 * 距離"] = df["距離"] * df["斤量"]
    df["斤量/馬体重 * 距離"] = df["距離"] * df["斤量/馬体重"]

    df["獲得賞金3"] = df["1前賞金"] + df["2前賞金"] + df["3前賞金"] 
    df["獲得賞金5"] = df["1前賞金"] + df["2前賞金"] + df["3前賞金"] + df["4前賞金"] + df["5前賞金"]
 
    sex_category = ["牝","牡","セ"]
    for i in range(1,4):
        for sex in sex_category:
            df.loc[df["性別"] == sex, sex + "_"+str(i)+"前レース間隔"] = df[str(i)+"前レース間隔"]

    prefix = ["1前着差","2前着差","3前着差","4前着差","5前着差"]
    df["5走最高着差"] = df[prefix].min(axis=1)
    df["5走最低着差"] = df[prefix].max(axis=1)

    prefix = ["1前ﾀｲﾑ指数","2前ﾀｲﾑ指数","3前ﾀｲﾑ指数","4前ﾀｲﾑ指数","5前ﾀｲﾑ指数"]
    df["5走最大ﾀｲﾑ指数"] = df[prefix].max(axis=1)
    df["5走最低ﾀｲﾑ指数"] = df[prefix].min(axis=1)

    prefix = ["1前上り","2前上り","3前上り","4前上り","5前上り"]
    df["5走最速上り"] = df[prefix].min(axis=1)


    df["1前_勝利時との斤量差分"] = df["斤量"] - df["1前_勝利時の斤量"]
    df["1前_勝利時との馬体重の差分"] = df["馬体重"] - df["1前_勝利時の馬体重"]
    df["1前_勝利時の日付"] = pd.to_datetime(df["1前_勝利時の日付"])        
    df["1前_勝利時からの間隔"] = (df["日付"] - df["1前_勝利時の日付"]).dt.days

    df["1前_複勝時との斤量差分"] = df["斤量"] - df["1前_複勝時の斤量"]
    df["1前_複勝時との馬体重の差分"] = df["馬体重"] - df["1前_複勝時の馬体重"]
    df["1前_複勝時の日付"] = pd.to_datetime(df["1前_複勝時の日付"])        
    df["1前_複勝時からの間隔"] = (df["日付"] - df["1前_複勝時の日付"]).dt.days

    df["日付-生年月日"] = (df["日付"] - df["生年月日"]).dt.days

    return df

def read(horse_filepath,race_filepath,o_filepath):
    
    df_h = pd.read_csv(horse_filepath)
    df_r = pd.read_csv(race_filepath)
    df = join(df_h,df_r)
    df = calc(df)
    df.to_csv(o_filepath,index=False)

