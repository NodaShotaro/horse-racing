
import requests
import pandas as pd
import numpy as np
import math
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime as dt

#import crowlhorse as ch

urlList = []
domain = "https://db.netkeiba.com/"


# ヘッダーの抽出
def extractHeader(thList):
    ans = []
    for th in thList:
        ans.append(th.text)
    return ans

def getSession(user,ps):

    # メイン
    login_info = {
        "pid":"login",
        "action":"auth",
        "mem_tp":"",
        "login_id":user,
        "pswd":ps,
    }

    session = requests.session()
    url_login ="https://regist.netkeiba.com/account/?pid=login"
    session.post(url_login, data=login_info)

    return session


def parseRaceURL(yRange):

    url_list = []
    domain = "https://db.netkeiba.com/"

    for year in range(yRange[0],yRange[1]):
        for month in range(1,13):
            for day in range(1,32):

                print(str(year) + "/" + str(month) + "/" + str(day))

                url = ""

                if (month < 10) & (day < 10):

                    url = "https://db.netkeiba.com/race/list/"+str(year)+"0"+str(month)+"0"+str(day)

                elif (month < 10) & (day >= 10):
                    url = "https://db.netkeiba.com/race/list/"+str(year)+"0"+str(month)+str(day)

                elif (month >= 10) & (day < 10):
                    url = "https://db.netkeiba.com/race/list/"+str(year)+str(month)+"0"+str(day)

                else:
                    url = "https://db.netkeiba.com/race/list/"+str(year)+str(month)+str(day)

                r = requests.get(url)
                soup = BeautifulSoup(r.content,"lxml")
                tagList = soup.find_all("dl",class_="race_top_data_info")

                if len(tagList) == 0:
                    continue
                else:           
                    print("hit")
                    for tag in tagList:
                            url_list.append(domain+tag.find("a")["href"])

    return url_list            

def parseBreederComment(session,url):

    r = session.get(url)
    soup = BeautifulSoup(r.content,"lxml")
    ans = ""

    x = soup.find_all("td",class_="bml")
    if len(x) != 1:
        print(x)
    else:
        ans = x[0].text
    
    return ans

def parseTraining(session,url):

    r = session.get(url)
    soup = BeautifulSoup(r.content,"lxml")
    ans = []

    # 馬名の取得
    horseName = soup.find_all("h1")[1].text.split(" ")[0].replace("\n","").strip("　")

    if "外" in soup.find_all("h1")[1].text:
        horseName = soup.find_all("h1")[1].text.split("外")[1].replace("\n","")

    elif "地" in soup.find_all("h1")[1].text:
        horseName = soup.find_all("h1")[1].text.split("地")[1].replace("\n","")

    elif "父" in soup.find_all("h1")[1].text:
        horseName = soup.find_all("h1")[1].text.split("父")[1].replace("\n","")

    else:
        horseName = soup.find_all("h1")[1].text.replace("\n","").replace(" ","")

    tables = soup.find_all("table",class_="race_table_01")

    for tab in tables:
        captionList = tab.find("caption").text.strip("\n").split("\xa0")
        date = captionList[0]
        place_r = captionList[2]
        
        x = tab.find_all("tr")
            
        header = extractHeader(x[0].find_all("th"))
        header = header[:len(header)-1]
        header.append("評価カテゴリ")
        header.append("映像")

        for row in x[1:]:
            result = {}
            result["レースの日付"] = date.split("(")[0]
            result["開催+R"] = place_r
            result["馬名"] = horseName

            cellList = row.find_all("td")

            for i in range(0,len(cellList)):
                if header[i] == "調教タイム":
                    timeList = cellList[i].find_all("li")

                    for j in range(0,len(timeList)):
                        result[header[i]+str(j+1)] = timeList[j].text
                
                else:
                    result[header[i]] = cellList[i].text

            ans.append(result)

    ans = pd.DataFrame(ans)
    return ans


def parseHorse(session,horse_url):

    domain = "https://db.netkeiba.com"

    result = {}

    r = session.get(horse_url)
    soup = BeautifulSoup(r.content,"lxml")

    result["毛色"] = soup.find("p",class_="txt_01").text.split("　")[2].strip(" ")
    horse_table = soup.find("table",class_="db_prof_table").find_all("tr")
    horseName = soup.find_all("h1")[1].text.split(" ")[0].replace("\n","")
    

    result["国際"] = 0.0
    result["地方"] = 0.0

    if len(horseName) > 1:  
        result["馬名"] = horseName

    elif "外" in soup.find_all("h1")[1].text:
        result["馬名"] = soup.find_all("h1")[1].text.split("外")[1].replace("\n","")
        result["国際"] = 1.0

    elif "地" in soup.find_all("h1")[1].text:
        result["馬名"] = soup.find_all("h1")[1].text.split("地")[1].replace("\n","")
        result["地方"] = 1.0

    elif "父" in soup.find_all("h1")[1].text:
        result["馬名"] = soup.find_all("h1")[1].text.split("父")[1].replace("\n","")

    else:
        result["馬名"] = soup.find_all("h1")[1].text.replace("\n","").replace(" ","")
        print(result["馬名"])


    is_birth = False
    is_breeder = False
    is_prod = False
    is_place = False
    is_owner = False

    for i in range(0,len(horse_table)):
        
        if horse_table[i].find("th").text.replace("\n","") == "生年月日":
            result["生年月日"] = horse_table[i].find("td").text.replace("\n","")
            is_birth = True

        elif horse_table[i].find("th").text.replace("\n","") == "調教師":
            result["調教師"] = horse_table[i].find("td").text.replace("\n","")
            result["所属"] = horse_table[1].find("td").text.split("(")[1].strip(")")
            is_breeder = True

        elif horse_table[i].find("th").text.replace("\n","") == "生産者":
            result["生産者"] = horse_table[i].find("td").text.replace("\n","")
            is_prod = True

        elif horse_table[i].find("th").text.replace("\n","") == "産地":
            result["産地"] = horse_table[i].find("td").text.replace("\n","")
            is_place = True

        elif horse_table[i].find("th").text.replace("\n","") == "馬主":
            result["馬主"] = horse_table[i].find("td").text.replace("\n","")
            is_owner = True

        if is_birth & is_breeder & is_place & is_prod & is_owner:
            break

    male_parent = soup.find("table",class_="blood_table").find_all("td",class_="b_ml")
    female_parent = soup.find("table",class_="blood_table").find_all("td",class_="b_fml")

    result["父"] = male_parent[0].find("a").text
    result["父父"] = male_parent[1].find("a").text
    result["母父"] = male_parent[2].find("a").text

    result["母"] = female_parent[1].find("a").text
    result["父母"] = female_parent[0].find("a").text
    result["母母"] = female_parent[2].find("a").text

    history = soup.find("table",class_="db_h_race_results")

    if history is None:
        resultList = [result]
        return pd.DataFrame(resultList)

    historyList = history.find_all("tr")
    header = []

    header = extractHeader(historyList[0].find_all("th"))

    preRaceList = []

    for row in historyList[1:]:
        
        preRace = {}
        cellList = row.find_all("td")
        cnt = 0

        for td in cellList:

            preRace[header[cnt]] = (td.text).replace("\n","")

            if header[cnt] == "レース名":
                preRace["レースのURL"] = domain + td.find("a")["href"]
        
            cnt = cnt + 1

        preRaceList.append(preRace)

    ans = pd.DataFrame(preRaceList)
    ans["毛色"] = result["毛色"]

    ans["父父"] = result["父父"]
    ans["母父"] = result["母父"]
    ans["父"] = result["父"]
    ans["母母"] = result["母母"]
    ans["母"] = result["母"]
    ans["父母"] = result["父母"]
    
    ans["馬名"] = result["馬名"]
    ans["生年月日"] = result["生年月日"]
    ans["所属"] = result["所属"]

    ans["生産者"] = result["生産者"]
    ans["産地"] = result["産地"]
    ans["馬主"] = result["馬主"]

    ans["地方"] = result["地方"]
    ans["国際"] = result["国際"]
    
    return ans


# レース結果ページのパース
def parseRaceResult(session,url):

    domain = "https://db.netkeiba.com"

    r = session.get(url)
    soup = BeautifulSoup(r.content,"lxml")

    main = soup.find("div",class_="mainrace_data")
    race_date = dt.strptime((main.find("p",class_="smalltxt").text).split(" ")[0],"%Y年%m月%d日")

    # レース結果の抽出
    originalTable = soup.find("table",class_="race_table_01")
    originalRow = originalTable.find_all("tr")
    resultList = []
    header = extractHeader(originalRow[0].find_all("th"))


    p_cnt = 1
    for row in originalRow[1:]:

#        print("\t"+str(p_cnt)+"/"+str(len(originalRow)-1))
        p_cnt = p_cnt + 1

        originalResult = row.find_all("td")
        result = {}
        cnt = 0

        for td in originalResult:
            result[header[cnt]] = (td.text).replace("\n","")

            if header[cnt] == "馬名":
                result["馬のURL"] = domain + td.find("a")["href"]

            elif (header[cnt] ==  "調教ﾀｲﾑ"):
                if td.find("a"):
                    result[header[cnt]] = domain + td.find("a")["href"]

            elif header[cnt] ==  "厩舎ｺﾒﾝﾄ":
                if td.find("a"):
                    result[header[cnt]] = domain + td.find("a")["href"]

            cnt = cnt + 1

        resultList.append(result)

    ans = pd.DataFrame(resultList)

    # レース条件の抽出
    active = soup.find_all("a",class_="active")
    race_round = ""
    
    if "R" in active[1].text:
        race_round = active[1].text

    elif "R" in active[0].text:
        race_round = active[0].text

    main = soup.find("div",class_="mainrace_data")
    title = main.find("h1").text

    x = (main.find("p",class_="smalltxt").text).split(" ")[1]
    place = re.search(r"(東京|京都|小倉|阪神|中山|中京|福島|新潟|札幌|函館)",x).group()

    race_date = dt.strptime((main.find("p",class_="smalltxt").text).split(" ")[0],"%Y年%m月%d日")
    race_cond = main.find_all("p")[1].text.split(" ")[2].split("\xa0")[0]
    attend_cond = main.find_all("p")[1].text.split(" ")[2].split("\xa0")[2]
    conditionList = (main.find("span").text).replace(" ","").split("/")
    course = conditionList[0].replace("\xa0","")

    if ":" in conditionList[1] : 
        ans["天気"] = conditionList[1].split(":")[1]
    else :
        ans["天気"] = ""

    if ":" in conditionList[2] :
        ans["馬"] = conditionList[2].split(":")[1]
    else :
        ans["馬場"] = ""

    race_date = dt.strptime((main.find("p",class_="smalltxt").text).split(" ")[0],"%Y年%m月%d日")
    race_cond = main.find("p",class_="smalltxt").text.split(" ")[2].split("\xa0")[0]

    if len(conditionList[3].split(":")) >= 2:
        ans["発走"] = conditionList[3].split(":")[1]
    else:
        ans["発走"] = "0"

    ans["開催"] = place
    ans["レース名"] = title
    ans["R"] = race_round
    ans["距離"] = course
    ans["日付"] = race_date
    ans["レースの階級"] = race_cond
    ans["出走条件"] = attend_cond

    if "右" in course:
        ans["左右"] = "右"
    elif "左" in course:
        ans["左右"] = "左"
    else:
        ans["左右"] = "直線"

    if "外" in course:
        ans["内外"] = "外"
    elif "内" in course:
        ans["内外"] = "内"
    else:
        ans["内外"] = "無"

    return pd.DataFrame(ans)
