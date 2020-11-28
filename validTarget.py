import glob
import pandas as pd
import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_list = glob.glob("dataset/result/*.csv")

df = pd.DataFrame()
for fname in csv_file_list:
    x = pd.read_csv(fname)
    x.rename(columns={
        "score_lgb_mean" : "勝_p_mean"
    },inplace=True)
    x = x[x["rank"]==1][["日付","開催","R","rank","馬番","馬名","勝_p_mean"]]
    x["勝_p_mean"] = round(x["勝_p_mean"],4)
    
    raceid = fname.split(".")[0].split("/")[2]
    if len(raceid) != 5:
        url = "https://race.netkeiba.com/race/result.html?race_id=20200"+raceid
    else:
        url = "https://race.netkeiba.com/race/result.html?race_id=2020100"+raceid

    print(url)

    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")
    trs = soup.find("table",class_="RaceTable01").find_all("tr")

    for tr in trs:
        if len(tr.find_all("td")) < 3:
            continue
        if tr.find_all("td")[2].find("div").text == str(x["馬番"].iloc[0,]):
            x["単勝"] = tr.find_all("td")[10].find("span").text
            x["着順"] = tr.find_all("td")[0].find("div").text
    df = pd.concat([x,df])

df.sort_values(["日付","開催","R"]).to_csv("demo.csv",index=False)
