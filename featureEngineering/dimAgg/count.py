import pandas as pd
import numpy as np

def initialize(df,category_name):

    prefix = category_name+"_昨年"    
    df[prefix+"勝数"] = np.nan
    df[prefix+"連対数"] = np.nan
    df[prefix+"複勝数"] = np.nan
    df[prefix+"2着数"] = np.nan
    df[prefix+"3着数"] = np.nan

    # 出走回数関連
    df[prefix+"出走回数"] = np.nan

    return df

def add(df,category_name,category_value,year):

    prefix = category_name+"_昨年"    

    df.loc[(df[category_name]==category_value) & (df["日付"].dt.year==year),prefix + "勝数"] = df[(df[category_name]==category_value) & (df["日付"].dt.year==year-1) & (df["着順"]==1)]["着順"].count()
    df.loc[(df[category_name]==category_value) & (df["日付"].dt.year==year),prefix + "連対数"] = df[(df[category_name]==category_value) & (df["日付"].dt.year==year-1) & (df["着順"]<=2)]["着順"].count()
    df.loc[(df[category_name]==category_value) & (df["日付"].dt.year==year),prefix + "複勝数"] = df[(df[category_name]==category_value) & (df["日付"].dt.year==year-1) & (df["着順"]<=3)]["着順"].count()
    df.loc[(df[category_name]==category_value) & (df["日付"].dt.year==year),prefix + "2着数"] = df[(df[category_name]==category_value) & (df["日付"].dt.year==year-1) & (df["着順"]==2)]["着順"].count()
    df.loc[(df[category_name]==category_value) & (df["日付"].dt.year==year),prefix + "3着数"] = df[(df[category_name]==category_value) & (df["日付"].dt.year==year-1) & (df["着順"]==3)]["着順"].count()
    df.loc[(df[category_name]==category_value) & (df["日付"].dt.year==year),prefix + "出走回数"] = df[(df[category_name]==category_value) & (df["日付"].dt.year==year-1)]["着順"].count()

    return df