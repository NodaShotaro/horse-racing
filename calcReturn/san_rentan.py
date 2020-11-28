
import pandas as pd
import lightgbm as lgb
import math
import os
import numpy as np

from datetime import datetime as dt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def calc3rentan(dfx):

    all_race_cnt = dfx[["開催","日付","R"]].drop_duplicates().count()["開催"]

    dfx["レース"] = dfx["開催"]+dfx["日付"].astype(str)+dfx["R"].astype(str)

    hit_cnt = 0
    back = 0
    backList = []
    for race in list(dfx["レース"].drop_duplicates()):
        
        target = dfx[dfx["レース"] == race]
        if len(target[(target["rank"] == 1.0) & (target["着順"] == 1.0)]) == 1 :
            if len(target[(target["rank"] == 2.0) & (target["着順"] == 2.0)]) == 1 :
                if len(target[(target["rank"] == 3.0) & (target["着順"] == 3.0)]) == 1 :
                    hit_cnt = hit_cnt + 1
                    back = back + target["三連単"].iloc[0,]
                    backList.append(target["三連単"].iloc[0,])

    print("三連単　的中率\t" + str(hit_cnt / all_race_cnt))
    print("三連単　回収率\t" + str(back / all_race_cnt) + "\n")

    back_std = pd.Series(backList).std()
    print("三連単　回収率\t" + str(back_std) + "\n")
