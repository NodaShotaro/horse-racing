
import pandas as pd
import numpy as np

def cutData(df):
       return df[~( (df["コースの種類"]=="障") | (df["レース条件"]=="新馬"))]

def splitAndSave(df):

       df["日付"] = pd.to_datetime(df["日付"])
       df = cutData(df)
       df["レース"] = df["日付"].astype("str") + "-" + df["R"].astype("str") + "-" + df["開催"]

       train1 = df[(df["日付"].dt.year == 2018)]
       train2 = df[(df["日付"].dt.year == 2019)]
       valid = df[(df["日付"].dt.year == 2020)]

       train1.sort_values(["レース","馬番"],inplace=True)
       train1.to_csv("dataset/train1.csv",index=False)
       train1["レース"].value_counts(sort=False).sort_index().to_csv("dataset/train1_query.csv",index=False)

       train2.sort_values(["レース","馬番"],inplace=True)
       train2.to_csv("dataset/train2.csv",index=False)
       train2["レース"].value_counts(sort=False).sort_index().to_csv("dataset/train2_query.csv",index=False)

       valid.sort_values(["レース","馬番"],inplace=True)
       valid.to_csv("dataset/valid.csv",index=False)
       valid["レース"].value_counts(sort=False).sort_index().to_csv("dataset/valid_query.csv",index=False)


def molding(filepath):
       df = pd.read_csv(filepath)
       splitAndSave(df)

