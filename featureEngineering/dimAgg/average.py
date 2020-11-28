import pandas as pd
import numpy as np


num_categories = [
    # レース前に分からないもの
    "着順",         "賞金",        
    "人気",         "単勝",   "ﾀｲﾑ指数",      
]

def initialize(df,category_name):

    prefix = category_name+"_昨年平均"    
    for num_category in num_categories:
        df[prefix + num_category] = np.nan
    return df

def add(df,category_name,category_value,year):

    prefix = category_name+"_昨年平均"
    for num_category in num_categories:
        df.loc[(df[category_name]==category_value) & (df["日付"].dt.year==year),prefix + num_category] = df[(df[category_name]==category_value) & (df["日付"].dt.year==year-1)][num_category].mean()

    return df