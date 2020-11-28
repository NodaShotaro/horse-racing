
import pandas as pd
import numpy as np
from calcReturn.single import calc

def load(data_path):

    df = pd.read_csv(data_path)
    df["回収"] = 0
    df.loc[df["着順"]==1,"回収"]=df["単勝"]

    return df

# def load(data_path):

#     df = pd.read_csv(data_path)
#     df["回収"] = 0
#     df.loc[df["着順"]==1,"回収"]=df["単勝"]
#     df.loc[df["単勝"]>=30,"回収"]=0

#     return df

def calcRet(df):
    
    return calc(df)

def checkReturnRate(df):

    lst = []

    lst.append(calcRet(df[df["所属"]=="栗東"]))
    lst.append(calcRet(df[(df["所属"]=="栗東") & (df["開催"]=="福島")]))
    lst.append(calcRet(df[df["地方"]==1.0]))
    lst.append(calcRet(df[df["国際"]==1.0]))
    lst.append(calcRet(df[df["馬番奇数"]==True]))

    lst.append(calcRet(df[df["1前馬場"]=="稍重"]))
    lst.append(calcRet(df[df["1前馬場"]=="不良"]))
    lst.append(calcRet(df[df["1前不利"]==True]))
    lst.append(calcRet(df[df["1前着順"]>=6]))
    lst.append(calcRet(df[df["1前着差"]>=3]))

    lst.append(calcRet(df[df["1前開催"]=="中山"]))
    lst.append(calcRet(df[df["1前開催"]=="京都"]))
    lst.append(calcRet(df[df["1前レース間隔"]>90]))
    lst.append(calcRet(df[df["馬体重の差分"]>10]))
    lst.append(calcRet(df[df["馬体重の差分"]<-10]))
    
    lst.append(calcRet(df[df["馬体重"]<450]))
    lst.append(calcRet(df[df["距離/1前"]>1]))
    lst.append(calcRet(df[(df["1前ペース(前半)"] >= df["1前ペース(後半)"])]))
    lst.append(calcRet(df[df["騎手"]=="池添謙一"]))
    lst.append(calcRet(df[df["騎手"]=="和田竜二"]))

    lst.append(calcRet(df[df["騎手"]=="岩田康誠"]))
    lst.append(calcRet(df[df["騎手"]=="藤田菜七"]))
    lst.append(calcRet(df[(df["1前人気"]==1) & (df["レース条件"]=="未勝利")]))
    lst.append(calcRet(df[df["年齢"]>5]))
    lst.append(calcRet(df[df["年齢"]==2]))

    lst.append(calcRet(df[(df["日付-生年月日"]<365*2.5)]))
    lst.append(calcRet(df[(df["馬名_出走回数"]==1)]))
    lst.append(calcRet(df[(df["馬名_出走回数"]>=5) & (df["馬名_出走回数"]<=7)]))
    lst.append(calcRet(df[(df["馬名_騎手_出走回数"] >= 5)]))
    lst.append(calcRet(df[(df["斤量-1前"] > 0)]))

    lst.append(calcRet(df[df["毛色"]=="青鹿毛"]))
    lst.append(calcRet(df[df["性別"]=="牝"]))
    lst.append(calcRet(df[df["1前馬場"]=="良"]))
    lst.append(calcRet(df[df["1前馬場"]=="重"]))
    lst.append(calcRet(df[(df["1前着差"]<=0.0) & (df["1前着順"]!=1)]))

    lst.append(calcRet(df[(df["所属"]=="美浦")]))
    lst.append(calcRet(df[(df["1前着順"]==1)]))
    lst.append(calcRet(df[(df["平均オッズ"]>=50)]))
    lst.append(calcRet(df[(df["開催"]=="中山") & (df["所属"]=="栗東")]))
    lst.append(calcRet(df[(df["1前レース間隔"]<10)]))

    lst.append(calcRet(df[(df["1前上り"]<34)]))
    lst.append(calcRet(df[(df["馬体重"] > 500)]))
    lst.append(calcRet(df[(df["斤量/馬体重"] >= 0.11)]))
    lst.append(calcRet(df[(df["1前頭数"] <= df["頭数"])]))
    lst.append(calcRet(df[(df["馬名_勝数"]==1) & (df["レース条件"] != "1勝")]))

    lst.append(calcRet(df[(df["馬名_開催_出走回数"] < 5)]))
    lst.append(calcRet(df[(df["馬名_複勝数"] >= 3)&(df["馬名_勝数"] == 0)]))
    lst.append(calcRet(df[(df["馬名_レース条件_出走回数"]>=5) & (df["レース条件"]=="1勝")]))
    lst.append(calcRet(df[(df["馬名_レース条件_出走回数"]>=5) & (df["レース条件"]=="2勝")]))
    lst.append(calcRet(df[(df["枠番"] <= 3)]))

    lst.append(calcRet(df[(df["枠番"] <= 2)]))
    lst.append(calcRet(df[(df["斤量"] <= 52)]))

    return lst

df = load("dataset/train1.csv")
df2 = load("dataset/train2.csv")

x = pd.DataFrame(checkReturnRate(df))
y = pd.DataFrame(checkReturnRate(df2))

print(pd.concat([x,y],axis=1))