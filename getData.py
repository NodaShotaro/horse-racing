
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime as dt

def extractEntered_N_Race(race_url,horse_url,n):

    domain = "https://db.netkeiba.com"

    r = requests.get(horse_url)
    soup = BeautifulSoup(r.content,"lxml")

    history = soup.find("table",class_="db_h_race_results")
    historyList = history.find_all("tr")

    header = []

    first = True
    race_cnt = 1
    rank_sum = 0
    extract_race = n
    race_flag = False

    for row in historyList:

        if first:
            first = False
            originalHeader = row.find_all("th")

            for th in originalHeader:
                header.append(th.text)
            continue

        result = {}
        originalResult = row.find_all("td")
        
        if race_flag:
            if race_cnt > extract_race:
                break
            else:
                cnt = 0                
                for td in originalResult:
                    if header[cnt] == "着順":
                        rank_sum = rank_sum + int(td.text)
                        break
                    cnt = cnt + 1
                race_cnt = race_cnt + 1
        else:
            cnt = 0
            for td in originalResult:
                if header[cnt] == "レース名":
                    if domain + td.find("a")["href"] == race_url:
                        print(td)
                        race_flag = True
                        break
                cnt = cnt + 1

    if race_cnt == 0:
        return 100
    else:
        return rank_sum / (race_cnt-1)


# 日付ごとのレース一覧をパース
# 例：https://db.netkeiba.com/race/list/20200125/
def parseRaceList(url):

    domain = "https://db.netkeiba.com"

    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")

    originalRaceListArea = soup.find("div",class_="race_list")
    originalRaceList = originalRaceListArea.find_all("li")

    urlList = []

    for race in originalRaceList:
        urlList.append(domain + race.find("a")["href"])

    return urlList

# レース結果ページのパース
# 例：https://db.netkeiba.com/race/202006010801/
def parseRaceResult(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")

    # レース結果の抽出
    originalTable = soup.find("table",class_="race_table_01")
    originalRow = originalTable.find_all("tr")
    resultList = []
    header = []
    first = True

    for row in originalRow:

        if first:

            originalHeader = row.find_all("th")
            
            for th in originalHeader:
                header.append(th.text)

            first = False
            continue

        originalResult = row.find_all("td")
        result = {}
        cnt = 0

        for td in originalResult:
            result[header[cnt]] = (td.text).replace("\n","")
   
            if header[cnt] == "馬名":
                result["3平均着順"] = extractEntered_N_Race(url,domain + td.find("a")["href"],3)
            cnt = cnt + 1


        resultList.append(result)

    ans = pd.DataFrame(resultList)


    # レース条件の抽出
    active = soup.find_all("a",class_="active")
    place = active[0].text
    race_round = active[1].text
    main = soup.find("div",class_="mainrace_data")
    title = main.find("h1").text

    conditionList = (main.find("span").text).replace(" ","").split("/")
    course = conditionList[0]

    if ":" in conditionList[1] : 
        ans["天候"] = conditionList[1].split(":")[1]
    else :
        ans["天候"] = ""

    if ":" in conditionList[2] :
        ans["地面"] = conditionList[2].split(":")[1]
    else :
        ans["地面"] = ""

    race_date = dt.strptime((main.find("p",class_="smalltxt").text).split(" ")[0],"%Y年%m月%d日")

    if len(conditionList[3].split(":")) >= 2:
        ans["発走"] = conditionList[3].split(":")[1]
    else:
        ans["発走"] = "0"

    ans["場所"] = place
    ans["レース名"] = title
    ans["ラウンド数"] = race_round
    ans["コース"] = course
    ans["日付"] = race_date

    return ans

# 馬ページのパース
# 例：https://db.netkeiba.com/horse/2014106220/

def parseHorse(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")

    history = soup.find("table",class_="db_h_race_results")
    historyList = history.find_all("tr")
    header = []
    resultList = []

    first = True

    for row in historyList:

        if first:
            first = False
            originalHeader = row.find_all("th")

            for th in originalHeader:
                header.append(th.text)
            continue

        result = {}
        originalResult = row.find_all("td")
        cnt = 0

        for td in originalResult:
            result[header[cnt]] = (td.text).replace("\n","")
            cnt = cnt + 1
        
        resultList.append(result)
    
    return pd.DataFrame(resultList)

def extractEnteredHorses(url):

    domain = "https://db.netkeiba.com"

    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")

    # レースに出場した馬の抽出
    originalTable = soup.find("table",class_="race_table_01")
    originalRow = originalTable.find_all("tr")
    horseUrlList = []
    first = True

    for row in originalRow:

        horse = row.find_all("td")
        if len(horse) == 21:
            url = horse[3].find("a")
            if url :
                horseUrlList.append(domain + url["href"])

    return horseUrlList

def extractEnteredRace(url):

    domain = "https://db.netkeiba.com"

    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")

    history = soup.find("table",class_="db_h_race_results")
    historyList = history.find_all("tr")
    header = []
    urlList = []

    first = True
    race_cnt = 0
    max_race = 10

    for row in historyList:

        if first:
            first = False
            originalHeader = row.find_all("th")

            for th in originalHeader:
                header.append(th.text)
            continue

        result = {}
        originalResult = row.find_all("td")
        cnt = 0

        if race_cnt > max_race:
            break
        
        for td in originalResult:
            if header[cnt] == "レース名":
                urlList.append(domain + td.find("a")["href"])
                break
            cnt = cnt + 1
        
        race_cnt = race_cnt + 1

    return urlList

# デモプログラム1

#url = "https://db.netkeiba.com/race/list/20200125/"
#urlList = parseRaceList(url)

# デモプログラム2

domain = "https://db.netkeiba.com"

urlList = ["https://db.netkeiba.com/horse/2014106220/",
"https://db.netkeiba.com/horse/2016104505/",
"https://db.netkeiba.com/horse/2016104854/",
"https://db.netkeiba.com/horse/2015105075/",
"https://db.netkeiba.com/horse/2014101976/",
"https://db.netkeiba.com/horse/2012104759/",
"https://db.netkeiba.com/horse/2014106201/",
"https://db.netkeiba.com/horse/2016104529/",
"https://db.netkeiba.com/horse/2015104961/",
"https://db.netkeiba.com/horse/2015104995/",
"https://db.netkeiba.com/horse/2014106046/",
"https://db.netkeiba.com/horse/2014106083/",
"https://db.netkeiba.com/horse/2014105517/",
"https://db.netkeiba.com/horse/2014105785/",
"https://db.netkeiba.com/horse/2015100600/",
"https://db.netkeiba.com/horse/2013102955/"
]
parseRaceList = []

# print("parse race1")
# for u in urlList:
#    parseRaceList.extend(extractEnteredRace(u))

# parseRaceList = list(set(parseRaceList))

# tmpHorseList = []

# print("parse horse")

# cnt = 1
# for u in parseRaceList:

#     print(str(cnt) + "/" + str(len(parseRaceList)))
#     cnt = cnt + 1
#     tmpHorseList.extend(extractEnteredHorses(u))
# urlList.extend(tmpHorseList)
# urlList = list(set(urlList))

print("parse race2")

cnt = 1
for u in urlList:

    print(str(cnt) + "/" + str(len(urlList)))
    cnt = cnt + 1
    parseRaceList.extend(extractEnteredRace(u))

parseRaceList = list(set(parseRaceList))

raceResultList = []
first = True
data = []

print("get data")

cnt = 1
for u in parseRaceList:

    print(str(cnt) + "/" + str(len(parseRaceList)))
    print(u)
    cnt = cnt + 1

    try:
        if first:
            data = parseRaceResult(u)
            first = False
        else:
            data = pd.concat([data,parseRaceResult(u)])

    except:
        print("skip!")
        print(u)

data["馬体重の増減"] = data[data["馬体重"].str.match(r"[0-9]+(.*)")]["馬体重"].str.split("(",expand=True)[1]
data["馬体重"] = data[data["馬体重"].str.match(r"[0-9]+(.*)")]["馬体重"].str.split("(",expand=True)[0]

data.to_csv("sample_horse.csv")