import pandas as pd
import numpy as np


num_categories = [
    # レース前に分かるもの
    "馬体重",       "斤量",     "馬体重の差分",  "頭数",             "枠番",
    "R",            "距離",

    # レース前に分からないもの
    "着順",         "着差",     "賞金",         "タイム(秒)",       "上り", 
    "スタート順位",  "通過1",    "通過2",        "通過3",            "通過4",
    "人気",         "オッズ",   "ﾀｲﾑ指数",      "馬場指数",
    "ペース(前半)",     "ペース(後半)",
]

def initialize(df):

    prefix = "平均"    
    for num_category in num_categories:
        df[prefix + num_category] = np.nan
    return df

def add(df,update_index,horseHist):

    prefix = "平均"
    for num_category in num_categories:
        df.at[update_index,prefix + num_category] = horseHist[num_category].mean()

    return df