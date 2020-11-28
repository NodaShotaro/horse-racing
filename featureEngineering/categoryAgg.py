
import pandas as pd
import numpy as np

from .dimAgg import average
from .dimAgg import count

def initialize(df,category_name):

    df = average.initialize(df,category_name)
    df = count.initialize(df,category_name)

    return df

def add(df,category_name,category_value,year):

    df = average.add(df,category_name,category_value,year)
    df = count.add(df,category_name,category_value,year)
            
    return df

def calc(df,category_name):

    df["日付"] = pd.to_datetime(df["日付"])

    year_list = list(set(df["日付"].dt.year))
    category_list = df[category_name].drop_duplicates()

    df = initialize(df,category_name)

    for i in range(0,len(category_list)):
        print(str(i) + "/" + str(len(category_list)) + "\t" + category_list.iloc[i,])
        for year in year_list:
            df = add(df,category_name,category_list.iloc[i,],year)
    return df
    
def read(i_filepath,o_filepath):
    
    df = pd.read_csv(i_filepath)
    df = calc(df,"騎手")
    df = calc(df,"調教師")
    df = calc(df,"馬主")
    # df = calc(df,"生産者")
    # df = calc(df,"父")
    # df = calc(df,"母")
    # df = calc(df,"父父")
    # df = calc(df,"父母")
    # df = calc(df,"母父")
    # df = calc(df,"母母")
    
    df.to_csv(o_filepath,index=False)

