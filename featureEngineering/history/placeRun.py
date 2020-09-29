import pandas as pd
import numpy as np

num_categories = ["斤量","馬体重","ﾀｲﾑ指数"]
str_categories = ["馬場","日付","距離カテゴリ","レース条件","開催"]

def initialize(df):
    for pre_pos in range(0,3):
        prefix = str(pre_pos+1)+"前_複勝時の"
        for str_category in str_categories:
            df[prefix + str_category] = None
        for num_category in num_categories:
            df[prefix + num_category] = np.nan
    return df

def add(df,update_index,horseHist):

    place = horseHist[(horseHist["着順"]<=3)]
    if len(place) <= 0:
        return df
    for pre_pos in range(0,3):
        if len(place) > pre_pos:
            prefix = str(pre_pos+1)+"前_複勝時の"
            for str_category in str_categories:
                df.at[update_index,prefix + str_category] = place[str_category].iloc[pre_pos,]
            for num_category in num_categories:
                df.at[update_index,prefix + num_category] = place[num_category].iloc[pre_pos,]
    return df