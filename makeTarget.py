
import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
from datetime import datetime

from crowling import parseNetkeiba
from featureEngineering import horseHistory
from featureEngineering import horseAgg
from featureEngineering import calcFeatures
from cleaning import cleanWrapper
from cleaning import clean

from predict import PredictionModel
from model.reg_timeindex import numFeature
from model.reg_timeindex import categoryFeature
from calcReturn import single

class makeTarget:

    def __init__(self):
        self.file_path = ""
    
    def setRaceUrl(self,race_url):
        self.race_url = race_url
        cnt = race_url[(len(race_url)-7):]
        cnt = str(int(cnt))
        self.file_path = "dataset/target/"+cnt+".csv"

    def getFilePath(self):
        return self.file_path

    def getSession(self):
        print("メールアドレス：")
        user = input()
        print("パスワード：")
        ps = input()
        self.session = parseNetkeiba.getSession(user,ps)

    def parseHorseList(self,horse_url_list):

        df = pd.DataFrame()
        for u in horse_url_list:
            df = pd.concat([parseNetkeiba.parseHorse(self.session,u),df])

        df.reset_index(drop=True,inplace=True)    

        return df

    def cleanRace(self,df):
        race_path = "dataset/dump/dump.csv"
        df.to_csv(race_path,index=False)
        df = clean.cleanSpaceAndLoad(race_path,race_path)
        df = cleanWrapper.cleanTarget(df)
        df.to_csv(race_path,index=False)
        df = pd.read_csv(race_path)
        return df

    def cleanHorse(self,df):
        race_path = "dataset/dump/dump.csv"
        df.to_csv(race_path,index=False)
        df = clean.cleanSpaceAndLoad(race_path,race_path)
        df = cleanWrapper.cleanHorseData(df)
        df.to_csv(race_path,index=False)
        df = pd.read_csv(race_path)
        return df

    def addHorseProf(self,df,df_h):
        prof_features = [
            "毛色",
            "父父",
            "母父",
            "父",
            "母母",
            "母",
            "父母",
            "馬名",
            "生年月日",
            "所属",
            "生産者",
            "産地",
            "馬主",
            "地方",
            "国際",
        ]

        horse_list = list(df["馬名"].drop_duplicates())
        print(list(df_h["馬名"].drop_duplicates()))
        
        for horse in horse_list:
            for prof in prof_features:
                df.loc[df["馬名"]==horse,prof] = df_h[df_h["馬名"]==horse][prof].iloc[0,]
        return df

    def exec(self,year,month,day):

        df = pd.DataFrame(parseNetkeiba.parseTargetRace(self.session,self.race_url))
        df_h = self.parseHorseList(list(df["馬のURL"]))

        df_h = self.cleanHorse(df_h)
        df = self.addHorseProf(df,df_h)
        df = self.cleanRace(df)

        df_h["日付"] = pd.to_datetime(df_h["日付"])
        df_h = df_h[(df_h["日付"] - datetime(year,month,day)).dt.days < 0]

        print("completed")
        df = pd.concat([df,df_h])
        df.reset_index(drop=True,inplace=True)
        df["日付"] = pd.to_datetime(df["日付"])

        df = horseHistory.calc(df)
        df = horseAgg.calc(df)
        df = df[(df["日付"] - datetime(year,month,day)).dt.days == 0]
        df["頭数"] = len(df)
        df = calcFeatures.calc(df)

        df.to_csv(self.file_path,index=False)

