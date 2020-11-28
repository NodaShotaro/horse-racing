
import pandas as pd
import parseNetkeiba
import sys

def crowlRace(session,race_url_list):

    lst = pd.DataFrame()
    cnt = 0
    end = len(race_url_list)
    for u in race_url_list:
        cnt = cnt + 1
        print(str(cnt) + "/" + str(end))
        lst = pd.concat([parseNetkeiba.parseRaceResult(session,u),lst])
    return lst

def crowlHorse(session,horse_url_list):

    lst = pd.DataFrame()
    cnt = 0
    end = len(horse_url_list)
    for u in horse_url_list:
        cnt = cnt + 1
        print(str(cnt) + "/" + str(end))
        lst = pd.concat([parseNetkeiba.parseHorse(session,u),lst])
        
    return lst

def crowlBlood(session,horse_url_list):

    lst = pd.DataFrame()
    cnt = 0
    end = len(horse_url_list)
    for u in horse_url_list:
        cnt = cnt + 1
        print(str(cnt) + "/" + str(end) +"\t" + u)
        lst = pd.concat([parseNetkeiba.parseBlood(session,u),lst])
    return lst

def crowlTraining(session,training_url_list):

    lst = pd.DataFrame()
    for u in training_url_list:
        time.sleep(0.5)
        lst = pd.concat([parseNetkeiba.parseTraining(session,u),lst])
    return lst

def crowlOdds(url_list):

    lst = []
    cnt = 0
    for u in url_list:
        cnt = cnt + 1
        print(str(cnt) + "/" + str(len(url_list)))
        lst.append(parseNetkeiba.parseOdds(u))
    
    return pd.DataFrame(lst)


def start():

    print("メールアドレス：")
    user = input()
    print("パスワード：")
    ps = input()
    session = parseNetkeiba.getSession(user,ps)

    # race_url_list = parseNetkeiba.parseRaceURL([2020,2021])
    # odds_data = crowlOdds(race_url_list)
    # odds_data.to_csv("result/Odds2020.csv",index=False)
    # race_data = crowlRace(session,race_url_list)
    # race_data.to_csv("result/raceTable.csv",index=False)

    race_data = pd.read_csv("result/raceTable.csv")
    horse_url_list = list(set(race_data["馬のURL"]))
    horse_data = crowlBlood(session,horse_url_list)
    horse_data.to_csv("result/bloodTable.csv",index=False)

    # training_url_list = list(race_data["調教ﾀｲﾑ"].drop_duplicates())
    # training_data = crowlHorse(session,training_url_list)
    # training_data.to_csv("result/trainingTable.csv",index=False)

start()