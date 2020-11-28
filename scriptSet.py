
import pandas as pd
import numpy as np
from calcReturn.single import calc
from calcReturn.single import calcAll

df = pd.read_csv("dataset/train1.csv")
df2 = pd.read_csv("dataset/train2.csv")

df["回収"] = 0
df2["回収"] = 0

df.loc[df["着順"]==1,"回収"]=df["単勝"]
df2.loc[df2["着順"]==1,"回収"]=df2["単勝"]

df.loc[df["単勝"]>=30,"回収"]=np.nan
df2.loc[df2["単勝"]>=30,"回収"]=np.nan

import pandas as pd
from datetime import datetime
from calcReturn.single import calc
from calcReturn.single import calcAll

df = pd.read_csv("result/predict.csv")
#df = pd.read_csv("dataset/valid.csv")

df["回収"] = 0
df.loc[df["着順"]==1,"回収"]=df["単勝"]
df[(df["単勝"]<=30) & (df["rank"]==1)]["回収"].mean()
df["日付"] = pd.to_datetime(df["日付"])

calcAll(df[(df["勝_p_mean"]>1.2) & (df["30倍以下_p_mean"]>0.8)])
calcAll(df[(df["勝_p_mean"]>1.2) & (df["1着率_p_mean"]>1.0) & (df["1着率_p_mean"] < 1.1)])