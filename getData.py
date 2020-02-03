
import requests
import pandas as pd
from bs4 import BeautifulSoup

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
            cnt = cnt + 1

        resultList.append(result)

    ans = pd.DataFrame(resultList)


    # レース条件の抽出
    place = soup.find("a",class_="active").text
    main = soup.find("div",class_="mainrace_data")
    title = main.find("h1").text

    conditionList = (main.find("span").text).replace(" ","").split("/")
    course = conditionList[0]
    weather = conditionList[1].split(":")[1]
    land_condition = conditionList[2].split(":")[1]
    
    if len(conditionList[3].split(":")) >= 2:
        ans["発走"] = conditionList[3].split(":")[1]
    else:
        ans["発走"] = "0"

    ans["場所"] = place
    ans["レース名"] = title
    ans["コース"] = course
    ans["天候"] = weather
    ans["地面"] = land_condition

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

def extractEnteredRace(url):

    domain = "https://db.netkeiba.com"

    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")

    history = soup.find("table",class_="db_h_race_results")
    historyList = history.find_all("tr")
    header = []
    urlList = []

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
            if header[cnt] == "レース名":
                urlList.append(domain + td.find("a")["href"])
                break
            cnt = cnt + 1

    return urlList


# デモプログラム1

#url = "https://db.netkeiba.com/race/list/20200125/"
#urlList = parseRaceList(url)

# デモプログラム2

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

for u in urlList:
    parseRaceList.extend(extractEnteredRace(u))

parseRaceList = list(set(parseRaceList))

raceResultList = []
first = True
data = []

for u in parseRaceList:

    print(u)

    if first:
        data = parseRaceResult(u)
        first = False
    else:
        data = pd.concat([data,parseRaceResult(u)])

data.to_csv("sample_horse.csv")


