import pandas as pd
import numpy as np

special_categories = ["レース間隔"]
num_categories = [
    "着順",         "着差",     "賞金",         "タイム(秒)",       "上り", 
    "スタート順位",  "通過1",    "通過2",        "通過3",            "通過4",
    "馬体重",       "斤量",     "馬体重の差分",  "ペース(前半)",     "ペース(後半)",
    "人気",         "オッズ",   "距離",         "頭数",             "枠番",
    "R",            "ﾀｲﾑ指数"
]
str_categories = [
    "日付",     "開催",     "馬場",     "天気",     "レース条件",   
    "出遅れ",   "不利",     "距離カテゴリ", "コースの種類",     "騎手"
]

def initialize(df):
    
    for pos in range(1,6):
        prefix = str(pos)+"前"
        for str_category in str_categories:
            df[prefix + str_category] = None
        for num_category in num_categories:
            df[prefix + num_category] = np.nan
        for special_category in special_categories:
            df[prefix + special_category] = np.nan
    return df

def add(df,update_index,horseHist):

    for pre_pos in range(0,5):
        prefix = str(pre_pos+1)+"前"
        if len(horseHist) > pre_pos:
            pre_index = horseHist.index[pre_pos]
            for str_category in str_categories:
                df.at[update_index,prefix + str_category] = horseHist.at[pre_index,str_category]
            for num_category in num_categories:
                df.at[update_index,prefix + num_category] = horseHist.at[pre_index,num_category]
            for special_category in special_categories:
                df.at[update_index,prefix + special_category] = (df.at[update_index,"日付"] - horseHist.at[pre_index,"日付"]).days

    return df