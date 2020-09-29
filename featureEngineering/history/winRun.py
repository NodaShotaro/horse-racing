import pandas as pd
import numpy as np

num_categories = ["斤量","馬体重","ﾀｲﾑ指数"]
str_categories = ["馬場","日付","距離カテゴリ","レース条件","開催"]
prefix = "1前_勝利時の"

def initialize(df):

    for str_category in str_categories:
        df[prefix + str_category] = None
    for num_category in num_categories:
        df[prefix + num_category] = np.nan
    return df

def add(df,update_index,horseHist):

    win = horseHist[(horseHist["着順"]==1)]
    if len(win) > 0:
        for str_category in str_categories:
            df.at[update_index,prefix + str_category] = win[str_category].iloc[0,]
        for num_category in num_categories:
            df.at[update_index,prefix + num_category] = win[num_category].iloc[0,]
    return df