
import requests
import pandas as pd
import numpy as np
import math
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime as dt

#import crowlhorse as ch


# ヘッダーの抽出
def extractHeader(thList):
    ans = []
    for th in thList:
        ans.append(th.text)
    return ans

def replaceJockey(df):

    dimName = "騎手"
    replaceList = [
        ["Ｓ．フォーリー","フォーリ"],
        ["Ｍ．デムーロ","Ｍ．デム"],
        ["Ｃ．ルメール","ルメール"],
        ["Ｆ．ミナリク","ミナリク"],
        ["Ａ．シュタルク","シュタル"],
        ["Ｌ．ヒューイットソン","ヒューイ"]
    ]

    for i in range(0,len(replaceList)):
        df[dimName] = df[dimName].str.replace(replaceList[i][0],replaceList[i][1])

    df[dimName] = df[dimName].str[:4]
    return df


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
    ans = addHorseProfile(ans,result)

    return ans

def addHorseProfile(df,prof_dict):

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
        "国際"
    ]
    for prof in prof_features:
        df[prof] = prof_dict[prof]

    return df

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
        ans["馬場"] = conditionList[2].split(":")[1]
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


def parseOdds(url):

    result = {}

    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")

    # オッズのパース
    tagList = soup.find_all("table",class_="pay_table_01")[0].find_all("tr")

    fukusho_odds = tagList[1].find_all("td")[1].get_text(".").replace(",","").split(".")

    # 代入
    result["複勝1"] = float(fukusho_odds[0]) / 100
    result["複勝2"] = float(fukusho_odds[1]) / 100
    if len(fukusho_odds) > 2:
        result["複勝3"] = float(fukusho_odds[2]) / 100

    if len(tagList) > 2:
        wakuren_odds = tagList[2].find_all("td")[1].text.replace(",","")
        result[tagList[2].find("th").text] = float(wakuren_odds) / 100

    if len(tagList) > 3:
        umaren_odds = tagList[3].find_all("td")[1].text.replace(",","")
        result[tagList[3].find("th").text] = float(umaren_odds) / 100

    tagList = soup.find_all("table",class_="pay_table_01")[1].find_all("tr")

    if tagList:
        
        wide_num = tagList[0].find_all("td")[0].get_text(".").split(".")
        wide_odds = tagList[0].find_all("td")[1].get_text(".").replace(",","").split(".")

        result["ワイド1-2"] = float(wide_odds[0]) / 100
        result["ワイド1-3"] = float(wide_odds[1]) / 100
        result["ワイド2-3"] = float(wide_odds[2]) / 100

        if len(tagList) > 1:
            umatan_odds = tagList[1].find_all("td")[1].text.replace(",","")
            result[tagList[1].find("th").text] = float(umatan_odds) / 100

            if len(tagList) > 2:
                sanpuku_odds = tagList[2].find_all("td")[1].text.replace(",","")
                result[tagList[2].find("th").text] = float(sanpuku_odds) / 100

                if len(tagList) > 3:
                    santan_odds = tagList[3].find_all("td")[1].text.replace(",","")
                    result[tagList[3].find("th").text] = float(santan_odds) / 100

    # 結合用のメタデータのパース
    
    main = soup.find("div",class_="mainrace_data")
    
    race_date = dt.strptime((main.find("p",class_="smalltxt").text).split(" ")[0],"%Y年%m月%d日")
    race_cond = main.find("p",class_="smalltxt").text.split(" ")[2].split("\xa0")[0]

    active = soup.find_all("a",class_="active")
    place = active[0].text
    race_round = active[1].text.replace("R","")

    result["日付"] = race_date
    result["開催"] = place
    result["R"] = race_round
    result["レース条件"] = race_cond
    return result


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

def parseBlood(session,horse_url):

    r = session.get(horse_url)
    soup = BeautifulSoup(r.content,"lxml")
    horseName = soup.find_all("h1")[1].text.split(" ")[0].replace("\n","")
    result = {}    

    # 名前情報のフォーマッティング
    if len(horseName) > 1:  
        result["馬名"] = horseName

    elif "外" in soup.find_all("h1")[1].text:
        result["馬名"] = soup.find_all("h1")[1].text.split("外")[1].replace("\n","")
    elif "地" in soup.find_all("h1")[1].text:
        result["馬名"] = soup.find_all("h1")[1].text.split("地")[1].replace("\n","")
    elif "父" in soup.find_all("h1")[1].text:
        result["馬名"] = soup.find_all("h1")[1].text.split("父")[1].replace("\n","")
    else:
        result["馬名"] = soup.find_all("h1")[1].text.replace("\n","").replace(" ","")
        print(result["馬名"])


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
    result["父"] = sire_list[0][0]
    result["母"] = mare_list[0][0]

    for i in range(1,5):
        prefix_list = makePrefix(i)
        for j in range(0,len(prefix_list)):
            result[prefix_list[j]+"父"] = sire_list[i][j]
            result[prefix_list[j]+"母"] = mare_list[i][j]
    df = pd.DataFrame([result])
    return df

def parseTargetRace(session,url):

    print(url)
    r = session.get(url)
    soup = BeautifulSoup(r.content,"lxml")

    horseList = soup.find("table",class_="Shutuba_Table").find_all("tr")
    horseList = horseList[2:]
    resultList = []
    horseUrlList = []
    jockeyUrlList = []

    domain = "https://db.netkeiba.com"

    cnt = 1
    for horse in horseList:

        print(str(cnt) +"/"+ str(len(horseList)))
        cnt = cnt +1

        result = {}

        cellList = horse.find_all("td")
        result["枠番"] = cellList[0].text
        result["馬番"] = cellList[1].text

        result["馬名"] = cellList[3].find("a").text.replace("　","")
        result["馬のURL"] = cellList[3].find("a")["href"]

        result["性齢"] = cellList[4].text.replace("\n","")
        result["斤量"] = cellList[5].text

        j_url = cellList[6].find("a")["href"]
        j_r = requests.get(j_url)
        jsoup = BeautifulSoup(j_r.content,"lxml")

        jockey_name = jsoup.find_all("h1")
        if len(jockey_name) > 0:
            jockey_name = jockey_name[1].text.replace("\n","").split(" ")[0]
            result["騎手"] = jsoup.find_all("h1")[1].text.replace("\n","").split(" ")[0]
        else:
            result["騎手"] = cellList[6].find("a").text

        b_url = cellList[7].find("a")["href"]
        b_r = requests.get(b_url)
        bsoup = BeautifulSoup(b_r.content,"lxml")
        breeder_name = bsoup.find_all("h1")
        if len(breeder_name) > 0:
            result["調教師"] = bsoup.find_all("h1")[1].text.replace("\n","").split(" ")[0]        
        else:
            result["調教師"] = cellList[7].find("a").text

        weight_str = cellList[8].text.replace("\n","")

        if len(weight_str) > 5:
            result["馬体重"] = weight_str.split("(")[0]
            result["馬体重の差分"] = weight_str.split("(")[1].replace(")","")
        else:
            result["馬体重"] = np.nan
            result["馬体重の差分"] = np.nan
            
        result["開催"] = soup.find_all("li",class_="Active")[0].text
        resultList.append(result)

    # 前処理
    df = pd.DataFrame(resultList)
    df["馬名"] = df["馬名"].str.strip(" ")
    df["馬名"] = df["馬名"].str.strip("　")

    date = soup.find("dd",class_="Active").text.split("(")[0]
    df["日付"] = dt.strptime("2020年"+date,"%Y年%m/%d")
    df["開催"] = soup.find("li",class_="Active").text
    
    condList = soup.find("div",class_="RaceData01").text.replace(" ","").replace("\n","").split("/")
    df["コースの種類"] = condList[1][:1]

    spanList = soup.find("div",class_="RaceData02").find_all("span")
    df["開催日数"] = re.search(r"([0-9]+)",spanList[2].text).group()
    df["開催回数"] = re.search(r"([0-9]+)",spanList[0].text).group()

    if "右" in condList[1]:
        df["左右"] = "右"
    elif "左" in condList[1]:
        df["左右"] = "左"
    else:
        df["左右"] = "直線"

    if "外" in condList[1]:
        df["内外"] = "外"
    elif "内" in condList[1]:
        df["内外"] = "内"
    else:
        df["内外"] = "無"

    df["距離"] = re.search(r"([0-9]+)",condList[1]).group()
    df["距離"] = df["距離"].astype("float")

    if len(condList) >= 3:
        df["天気"] = condList[2].split(":")[1]
        df["馬場"] = condList[3].split(":")[1]
        df["馬場"] = df["馬場"].str.replace("不","不良")
        df["馬場"] = df["馬場"].str.replace("稍","稍重")
    else:
        df["天気"] = "晴"
        df["馬場"] = "良"

    df["R"] = soup.find_all("li",class_="Active")[1].text.strip("\n").strip("R")
    df["R"] = df["R"].astype("int")
    raceCond = soup.find_all("div",class_="RaceName")[0].text.replace("\n","")
    df["レース名"] = raceCond
     
    if soup.find("span",class_="Icon_GradeType1"):
        df["レース条件"] = "G1"
    elif soup.find("span",class_="Icon_GradeType2"):
        df["レース条件"] = "G2"
    elif soup.find("span",class_="Icon_GradeType3"):
        df["レース条件"] = "G3"
    else:
        if "未勝利" in raceCond:
            df["レース条件"] = "未勝利"
        elif "新馬" in raceCond:
            df["レース条件"] = "新馬"
        elif "1勝" in raceCond:
            df["レース条件"] = "1勝"
        elif "2勝" in raceCond:
            df["レース条件"] = "2勝"
        elif "3勝" in raceCond:
            df["レース条件"] = "3勝"
        else:
            df["レース条件"] = "名前付き"

    df = replaceJockey(df)
    return df