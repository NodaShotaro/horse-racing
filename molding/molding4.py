
import pandas as pd
import numpy as np

def cutData(df):
       return df[~( (df["コースの種類"]=="障") | (df["レース条件"]=="新馬"))]

def splitAndSave(df):

       df["日付"] = pd.to_datetime(df["日付"])
       df = cutData(df)
       df["レース"] = df["日付"].astype("str") + "-" + df["R"].astype("str") + "-" + df["開催"]

       train1 = df[(df["日付"].dt.year == 2018) & (df["日付"].dt.month <= 6)]
       train2 = df[(df["日付"].dt.year == 2018) & (df["日付"].dt.month > 6)]
       train3 = df[(df["日付"].dt.year == 2019) & (df["日付"].dt.month <= 6)]
       train4 = df[(df["日付"].dt.year == 2019) & (df["日付"].dt.month > 6)]
       valid = df[(df["日付"].dt.year == 2020)]

       train1.sort_values(["レース","馬番"],inplace=True)
       train1.to_csv("dataset/train1.csv",index=False)
       train1["レース"].value_counts(sort=False).sort_index().to_csv("dataset/train1_query.csv",index=False)

       train2.sort_values(["レース","馬番"],inplace=True)
       train2.to_csv("dataset/train2.csv",index=False)
       train2["レース"].value_counts(sort=False).sort_index().to_csv("dataset/train2_query.csv",index=False)

       train3.sort_values(["レース","馬番"],inplace=True)
       train3.to_csv("dataset/train3.csv",index=False)
       train3["レース"].value_counts(sort=False).sort_index().to_csv("dataset/train3_query.csv",index=False)

       train4.sort_values(["レース","馬番"],inplace=True)
       train4.to_csv("dataset/train4.csv",index=False)
       train4["レース"].value_counts(sort=False).sort_index().to_csv("dataset/train4_query.csv",index=False)

       valid.sort_values(["レース","馬番"],inplace=True)
       valid.to_csv("dataset/valid.csv",index=False)
       valid["レース"].value_counts(sort=False).sort_index().to_csv("dataset/valid_query.csv",index=False)


def molding(filepath,bloodpath):
       df = pd.read_csv(filepath)
       dx = pd.read_csv(bloodpath)
       splitAndSave(pd.merge(df,dx))

