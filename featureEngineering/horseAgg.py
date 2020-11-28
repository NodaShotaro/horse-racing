
import pandas as pd
import numpy as np

from .agg import average
from .agg import count

def initialize(df):

    df = average.initialize(df)
    df = count.initialize(df)

    return df

def add(df,update_index,horseHist):

    df = average.add(df,update_index,horseHist)
    df = count.add(df,update_index,horseHist)
            
    return df

def calc(df):

    df["日付"] = pd.to_datetime(df["日付"])
    df.sort_values("日付",ascending=False,inplace=True)

    horseList = df["馬名"].drop_duplicates()
    df = initialize(df)

    for i in range(0,len(horseList)):
        
        horse_t = df[df["馬名"] == horseList.iloc[i,]]
        print(str(i) + "/" + str(len(horseList)) + "\t" + horseList.iloc[i,])

        for pos in range(0,len(horse_t)):        

            if len(horse_t.iloc[pos:]) > 1:

                update_index = horse_t.index[pos]
                horseHist = horse_t.iloc[pos+1:,:]

                df = add(df,update_index,horseHist)

    return df
    
def read(i_filepath,o_filepath):
    
    df = pd.read_csv(i_filepath)
    df = calc(df)
    df.to_csv(o_filepath,index=False)

