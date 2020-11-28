import glob
import pandas as pd
import requests
import pandas as pd
from bs4 import BeautifulSoup

def setRaceUrl(race_url):

    cnt = race_url[(len(race_url)-7):]
    cnt = str(int(cnt))
    file_path = "dataset/result/"+cnt+".csv"

    return file_path


urls = [    
    "https://race.netkeiba.com/race/shutuba.html?race_id=202005050601",
    "https://race.netkeiba.com/race/shutuba.html?race_id=202009050601",

    "https://race.netkeiba.com/race/shutuba.html?race_id=202005050602",
    "https://race.netkeiba.com/race/shutuba.html?race_id=202009050602",

    "https://race.netkeiba.com/race/shutuba.html?race_id=202005050603",
    "https://race.netkeiba.com/race/shutuba.html?race_id=202009050603",

    "https://race.netkeiba.com/race/shutuba.html?race_id=202009050604",

    "https://race.netkeiba.com/race/shutuba.html?race_id=202005050607",
    "https://race.netkeiba.com/race/shutuba.html?race_id=202009050607",

    "https://race.netkeiba.com/race/shutuba.html?race_id=202005050608",
    "https://race.netkeiba.com/race/shutuba.html?race_id=202009050608",

    "https://race.netkeiba.com/race/shutuba.html?race_id=202005050609",
    "https://race.netkeiba.com/race/shutuba.html?race_id=202009050609",

    "https://race.netkeiba.com/race/shutuba.html?race_id=202005050610",
    "https://race.netkeiba.com/race/shutuba.html?race_id=202009050610",

    "https://race.netkeiba.com/race/shutuba.html?race_id=202005050611",
    "https://race.netkeiba.com/race/shutuba.html?race_id=202009050611",

    "https://race.netkeiba.com/race/shutuba.html?race_id=202005050612",
    "https://race.netkeiba.com/race/shutuba.html?race_id=202009050612",

]



files = []

for u in urls:
    files.append(setRaceUrl(u))

df = pd.DataFrame()
for fname in files:
    x = pd.read_csv(fname)
    x = x[(x["勝_p_mean"] > 1.1) | (x["rank"]<=2)]
    df = pd.concat([x,df])

df[["日付","開催","R","rank","馬番","馬名","勝_p_mean"]].sort_values(["開催","R"]).to_csv("demo.csv",index=False)
