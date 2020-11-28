import pandas as pd
import numpy as np
from datetime import datetime as dt

from calcReturn import single
from calcReturn import multi
from calcReturn import umaren
from calcReturn import wide
from calcReturn import san_renpuku
from calcReturn import san_rentan

df = pd.read_csv("result/predict.csv")
dx = pd.read_csv("crowling/result/Odds2020.csv")
dx.drop("レース条件",axis=1,inplace=True)

df["日付"] = pd.to_datetime(df["日付"])
dx["日付"] = pd.to_datetime(dx["日付"])

dx.loc[dx["R"]=="結果/払戻","R"] = dx["開催"]
dx.loc[dx["R"]=="結果/払戻","開催"] = "中山"
dx["R"] = dx["R"].str.replace("R","")
dx["R"] = dx["R"].astype("int")

df = pd.merge(df,dx,on=["日付","開催","R"])
multi.calcMulti(df[(df["勝_p_mean"]>1.2) & (df["単勝"]>20) & (df["単勝"] < 100)])
# umaren.calcUmaren(df)

