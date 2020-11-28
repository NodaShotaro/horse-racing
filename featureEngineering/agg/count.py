import pandas as pd
import numpy as np

str_categories = [
    "開催",     "馬場",     "レース条件",   
    "距離カテゴリ", "コースの種類",     "騎手"
]

def initialize(df):

    prefix = "馬名_"    

    # 着順から作成したもの
    df[prefix+"勝数"] = np.nan
    df[prefix+"連対数"] = np.nan
    df[prefix+"複勝数"] = np.nan
    df[prefix+"2着数"] = np.nan
    df[prefix+"3着数"] = np.nan

    # 出走回数関連
    df[prefix+"出走回数"] = np.nan
    for str_category in str_categories:
        df[prefix+str_category+"_出走回数"] = np.nan

    return df

def add(df,update_index,horseHist):

    prefix = "馬名_"    

    # 着順から作成したもの
    df.at[update_index,prefix + "勝数"] = horseHist[horseHist["着順"]==1]["着順"].count()
    df.at[update_index,prefix + "連対数"] = horseHist[horseHist["着順"]<=2]["着順"].count()
    df.at[update_index,prefix + "複勝数"] = horseHist[horseHist["着順"]<=3]["着順"].count()
    df.at[update_index,prefix + "2着数"] = horseHist[horseHist["着順"]==2]["着順"].count()
    df.at[update_index,prefix + "3着数"] = horseHist[horseHist["着順"]==3]["着順"].count()

    # 出走回数関連
    df.at[update_index,prefix + "出走回数"] = horseHist["着順"].count()
    for str_category in str_categories:
        df.at[update_index,prefix+str_category+"_出走回数"] = horseHist[horseHist[str_category] == df.at[update_index,str_category]][str_category].count()

    return df