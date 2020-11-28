import requests
import pandas as pd
import numpy as np
import math
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime as dt

def makePrefix(length):
    candidates = ["父","母"]
    prefix_list = ["父","母"]
    tmp = []

    for i in range(0,length-1):
        for prefix in prefix_list:
            for candidate in candidates:
                tmp.append(prefix+candidate)
        prefix_list = tmp
        tmp = []

    return prefix_list

def convertHorseUrl2Blood(url):
    return url.replace("horse","horse/ped")

def parseBlood(horse_url,df):

    url = convertHorseUrl2Blood(horse_url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")

    sire_list = [[],[],[],[],[]]
    mare_list = [[],[],[],[],[]]

    trs = soup.find("table",class_="blood_table").find_all("tr")

    for i in range(0,len(trs)):
        tds = trs[i].find_all("td")
        tds.reverse()

        for j in range(0,len(tds)):
            if i % (2 ** (j+1)) == 0:
                link = tds[j].find("a")
                if link:
                    sire_list[j].append(link.text.replace("\n",""))
                else:
                    sire_list[j].append("")
            else:
                link = tds[j].find("a")
                if link:
                    mare_list[j].append(link.text.replace("\n",""))
                else:
                    mare_list[j].append("")

    sire_list.reverse()
    mare_list.reverse()

    df["父"] = sire_list[0][0]
    df["母"] = mare_list[0][0]

    for i in range(1,5):
        prefix_list = makePrefix(i)
        for j in range(0,len(prefix_list)):
            df[prefix_list[j]+"父"] = sire_list[i][j]
            df[prefix_list[j]+"母"] = mare_list[i][j]
    print(df)
    return df

horse_url = "https://db.netkeiba.com/horse/2015106216/"

df = pd.DataFrame([{"馬名" : "コントレイル"}])
print(df)
df = parseBlood(horse_url,df)
print(df)