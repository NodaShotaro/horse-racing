import pandas as pd
import numpy as np

def join(df_h,df_r):

       df_h.drop(['天気','枠番',"馬番", 'オッズ', '人気','不利',"出遅れ","ﾀｲﾑ指数","距離カテゴリ",
              '着順', '騎手', '斤量', '距離', '馬場', 'タイム', '通過', '上り', '馬体重',
              '賞金','コースの種類', 'ペース(前半)', 'ペース(後半)',
              '馬体重の差分'],axis=1,inplace=True)

       df_r.drop(["レース名"],axis=1,inplace=True)

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

    # 所属系列
    df["所属*開催"] = df["所属"] + df["開催"]
    df["所属*距離カテゴリ"] = df["所属"] + df["距離カテゴリ"].astype("str")

    return df

def makeSameCondLast(df):
    str_categories = [
        "開催",
        "レース条件",
        "距離カテゴリ",
        "コースの種類",
        "騎手"
    ]
    for str_category in str_categories:
        df["=1前"+str_category] = df[str_category] == df["1前"+str_category]

    return df
    
def makeLastPerNow(df):
    num_categories = [
        "馬体重","馬体重の差分","斤量","頭数","枠番","R","距離",
    ]
    for num_category in num_categories:
        df[num_category+"/1前"] = df[num_category] / df["1前"+num_category]
        df[num_category+"-1前"] = df[num_category] - df["1前"+num_category]
    return df

def makeLastNAgg(df,dim_name,n):
    dim_list = []    
    for i in range(1,n+1):
        dim_list.append(str(i)+"前"+dim_name)

    df[str(n)+"走最大"+dim_name] = df[dim_list].min(axis=1)
    df[str(n)+"走最小"+dim_name] = df[dim_list].max(axis=1)

    return df

def calc(df):

    ## 前処理
    df["日付"] = pd.to_datetime(df["日付"])
    df["生年月日"] = pd.to_datetime(df["生年月日"],format="%Y年%m月%d日")
    df["距離"] = df["距離"].astype("int")
    df["枠番"] = df["枠番"].astype("int")
    df["馬番"] = df["馬番"].astype("int")
    df["年齢"] = df["年齢"].astype("int")
    df["性別+月"] = df["性別"] + (df["日付"].dt.month).astype("str")

    print(df)

    df = makeCrossCategory(df)
    df = makeSameCondLast(df)
    df = makeLastPerNow(df)

    df["馬番奇数"] = df["馬番"] % 2 == 1

    # 1前の系列
    df["1前着順-人気"] = df["1前着順"] - df["1前人気"]

    # 馬体重の系列
    df["馬体重の差分/馬体重"] = df["馬体重の差分"] / df["馬体重"]
    df["斤量/馬体重"] = df["斤量"] / df["馬体重"]

    df["(馬体重+斤量)-1前"] = df["馬体重-1前"] + df["斤量-1前"]

    df["馬体重 * 距離"] = df["距離"] * df["馬体重"]
    df["斤量 * 距離"] = df["距離"] * df["斤量"]
    df["馬体重の差分 * 距離"] = df["距離"] * df["馬体重の差分"]
    df["斤量/馬体重 * 距離"] = df["距離"] * df["斤量/馬体重"]
    df["距離/1前 * 馬体重の差分/馬体重"] = df["距離/1前"] * df["馬体重の差分/馬体重"]

    # 枠番の系列
    df["開催日数/枠番"] = df["開催日数"] / df["枠番"]
    df["開催日数*枠番"] = df["開催日数"] * df["枠番"]
    df["開催日数*枠番+R"] = df["開催日数"] * df["枠番"] + df["R"]
    df["開催日数*枠番*R"] = df["開催日数"] * df["枠番"] * df["R"]

    df["獲得賞金3"] = df["1前賞金"] + df["2前賞金"] + df["3前賞金"] 
    df["獲得賞金5"] = df["1前賞金"] + df["2前賞金"] + df["3前賞金"] + df["4前賞金"] + df["5前賞金"]
 
    sex_category = ["牝","牡","セ"]
    for i in range(1,4):
        for sex in sex_category:
            df.loc[df["性別"] == sex, sex + "_"+str(i)+"前レース間隔"] = df[str(i)+"前レース間隔"]

    df = makeLastNAgg(df,"着差",3)
    df = makeLastNAgg(df,"着差",5)
    df = makeLastNAgg(df,"着順",3)
    df = makeLastNAgg(df,"着順",5)
    df = makeLastNAgg(df,"ﾀｲﾑ指数",3)
    df = makeLastNAgg(df,"ﾀｲﾑ指数",5)
    df = makeLastNAgg(df,"上り",3)
    df = makeLastNAgg(df,"上り",5)
    df = makeLastNAgg(df,"人気",3)
    df = makeLastNAgg(df,"人気",5)
    df = makeLastNAgg(df,"オッズ",3)
    df = makeLastNAgg(df,"オッズ",5)
    df = makeLastNAgg(df,"スタート順位",3)
    df = makeLastNAgg(df,"スタート順位",5)
    df = makeLastNAgg(df,"通過4",3)
    df = makeLastNAgg(df,"通過4",5)

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

