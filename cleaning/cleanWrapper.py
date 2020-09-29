
import pandas as pd
from . import clean
from . import encode

def cleanRaceData(df):

    df["日付"] = pd.to_datetime(df["日付"])

    df.rename(columns= {
        "賞金(万円)" : "賞金",
        },inplace=True)

    df["単勝"] = df["単勝"].astype("str")
    df["単勝"] = df["単勝"].str.replace("---","")
    df["調教師"] = df["調教師"].str.split("]",expand=True)[1]
    df["R"] = df["R"].str.replace("R","")
    df["性別"] = df["性齢"].str[:1] 
    df["年齢"] = df["性齢"].str[1:] 

    df = clean.cleanRank(df)
    df = clean.cleanRewards(df)
    df = clean.cleanRemarks(df)
    df = clean.cleanHorseWeight(df)
    df = clean.cleanCourseDist(df)

    df = encode.courseCategory(df)
    df["コースと枠"] = df["開催"] +"-"+ df["内外"] +"-"+ df["コースの種類"] + "-" + df["距離"].astype("str") +"-"+ df["枠番"].astype("str")

    drop_features = [
        "着差",     "備考",
        "厩舎ｺﾒﾝﾄ", "調教ﾀｲﾑ",
        "馬のURL",
        "性齢",
        "通過",
        "上り",
    ]
    df = clean.dropFeatures(df,drop_features,)

    return df

def cleanHorseData(df):

    df["日付"] = pd.to_datetime(df["日付"])

    df = clean.cleanRank(df)
    df = clean.cleanCornerRank(df)
    df = clean.cleanTime(df)
    df = clean.cleanHorseWeight(df)
    df = clean.cleanHorseName(df)
    df = clean.cleanRemarks(df)
    df = clean.cleanRewards(df)
    df = clean.cleanHeld(df)
    df = clean.cleanCourseDist(df)
    df = clean.cleanBaba(df)
    df = clean.cleanPace(df)

    df = encode.raceCond(df)
    df = encode.courseCategory(df)
    df = encode.paceCategory(df)
    df = encode.footStyle(df)

    df.loc[df["着順"] == 1,"回収"] = df["オッズ"]
    df["回収"].fillna(0,inplace=True)

    drop_features = [
        "馬主",         "備考",
        "レースのURL",  "映像",
        "勝ち馬(2着馬)", "ペース",
        "厩舎ｺﾒﾝﾄ",
    ]
    df = clean.dropFeatures(df,drop_features)
    df.drop_duplicates(inplace=True)

    return df

def cleanTrainData(df):

    df["R"] = df["開催+R"].str.extract("([0-9]+)")
    df["開催"] = df["開催+R"].str[:2]
    df.rename(columns= {
        "日付" : "調教の日付",
        "レースの日付" : "日付",
        "コース" : "調教コース",
        "馬場" : "調教の馬場",
        },inplace=True)

    df.drop("開催+R",axis=1,inplace=True)

    df["日付"] = pd.to_datetime(df["日付"])

    df = clean.cleanHorseName(df)

    df["調教の日付"] = df["調教の日付"].str.split("(",expand=True)[0]
    df["調教の日付"] = pd.to_datetime(df["調教の日付"])
    df["調教からの日数"] = (df["日付"] - df["調教の日付"]).dt.days

    df["レースから見て何回目の調教か"] = df.groupby(["馬名","日付","開催","R"])["調教からの日数"].rank()
    df = df[df["レースから見て何回目の調教か"] == 1]
    df.drop("レースから見て何回目の調教か",axis=1,inplace=True)


    df["計測不能"] = df["調教タイム5"].str.contains("(計時不能|計不|見えず)")
    df["中間軽め"] = df["調教タイム5"].str.contains("(中間)")
    df["障害練習"] = df["調教タイム5"].str.contains("(障害|飛越)")

    for i in range(1,6):

        df["調教タイム"+str(i)] = df["調教タイム"+str(i)].str.replace("\?","")
        df["調教タイム"+str(i)] = df["調教タイム"+str(i)].str.replace("ユキ","")
        df["調教タイム"+str(i)] = df["調教タイム"+str(i)].str.replace("モヤ","")

        df.loc[df["調教タイム"+str(i)].str.contains("走試")==True,"走試"] = True
        df.loc[df["調教タイム"+str(i)].str.contains("ゲート")==True,"ゲート"] = True

        df["調教タイム"+str(i)] = df["調教タイム"+str(i)].str.replace("走試","")
        df["調教タイム"+str(i)] = df["調教タイム"+str(i)].str.replace("ゲート","")
        df["調教タイム"+str(i)] = df["調教タイム"+str(i)].str.replace("-","")

        # 調教回数を格納し，調教タイムからは削除
        df["buf"] = df["調教タイム"+str(i)].str.extract("(\([0-9]\))")
        df["buf"] = df["buf"].str.extract("([0-9])").astype("float")
        df.loc[~(np.isnan(df["buf"])),"調教回数"] = df["buf"]
        df["調教タイム"+str(i)] = df["調教タイム"+str(i)].str.replace("\([0-9]\)","")

    # 障害試験のタイムは調教タイム_障へ残し，調教タイムは普段のものを格納
    if len(df[df["調教タイム3"].str.contains("障試")==True]) >= 1:
        df.loc[df["調教タイム3"].str.contains("障試")==True,"調教タイム_障"] = df["調教タイム3"].str.split("障試",expand=True)[1]    
    if len(df[df["調教タイム4"].str.contains("障試")==True]) >= 1:
        df.loc[df["調教タイム4"].str.contains("障試")==True,"調教タイム_障"] = df["調教タイム4"].str.split("障試",expand=True)[1]
    for i in range(1,6):
        df.loc[df["調教タイム"+str(i)].str.contains("障試")==True,"調教タイム"+str(i)] = df["調教タイム"+str(i)].str.split("障試",expand=True)[0]
    
    # 調教回数がもしnullだったら1に置換
    df.drop("buf",axis=1,inplace=True)
    df.loc[~(np.isnan(df["調教回数"])),"調教回数"] = 1

    # 調教タイムが途中で測れなくなってラップタイムになったケースの対処
    for i in range(1,6):
        for j in range (2,6):
            if i == j:   
                df.loc[df["調教タイム"+str(j)].str.contains("ラップ")==True,"調教ラップ"+str(j)] = df["調教タイム"+str(j)].str.replace("ラップ","")
            df.loc[df["調教タイム"+str(i)].str.contains("ラップ")==True,"調教ラップ"+str(j)] = df["調教タイム"+str(j)]
            df.loc[df["調教タイム"+str(i)].str.contains("ラップ")==True,"調教タイム"+str(j)] = np.nan

    for i in range(1,6):
        df["調教タイム"+str(i)] = df["調教タイム"+str(i)].str.replace("計不","")
        df["調教ラップ"+str(i)] = df["調教ラップ"+str(i)].str.replace("計不","")    

    # 調教タイム5に出てくる文字列の削除
    df["調教タイム5"] = df["調教タイム5"].str.replace("は","")
    df["調教タイム5"] = df["調教タイム5"].str.replace("連闘の疲れ見せずに元気に坂路","")
    df.loc[df["計測不能"]==True,"調教タイム5"] = np.nan
    df.loc[df["中間軽め"]==True,"調教タイム5"] = np.nan
    df.loc[df["障害練習"]==True,"調教タイム5"] = np.nan

    # 調教タイムの型の変換
    for i in range(1,6):

        df.loc[df["調教タイム"+str(i)]=="","調教タイム"+str(i)] = np.nan
        df.loc[df["調教ラップ"+str(i)]=="","調教ラップ"+str(i)] = np.nan
        
        df["調教タイム"+str(i)] = df["調教タイム"+str(i)].astype("float")
        df["調教ラップ"+str(i)] = df["調教ラップ"+str(i)].astype("float")

    df.loc[(np.isnan(df["調教ラップ1"])) & ~(np.isnan(df["調教タイム1"])) & ~(np.isnan(df["調教タイム2"])),"調教ラップ1"] = df["調教タイム1"] - df["調教タイム2"]
    df.loc[(np.isnan(df["調教ラップ2"])) & ~(np.isnan(df["調教タイム2"])) & ~(np.isnan(df["調教タイム3"])),"調教ラップ2"] = df["調教タイム2"] - df["調教タイム3"]
    df.loc[(np.isnan(df["調教ラップ3"])) & ~(np.isnan(df["調教タイム3"])) & ~(np.isnan(df["調教タイム4"])),"調教ラップ3"] = df["調教タイム3"] - df["調教タイム4"]
    df.loc[(np.isnan(df["調教ラップ4"])) & ~(np.isnan(df["調教タイム4"])) & ~(np.isnan(df["調教タイム5"])),"調教ラップ4"] = df["調教タイム4"] - df["調教タイム5"]

    df.loc[df["調教コース"].str.contains("(北|南|美|障芝|飛芝)")==True,"調教場所"] = "美浦"
    df.loc[df["調教コース"].str.contains("(栗|ＣＷ|ＤＰ)")==True,"調教場所"] = "栗東"
    df.loc[df["調教コース"].str.contains("(函)")==True,"調教場所"] = "函館"
    df.loc[df["調教コース"].str.contains("(札)")==True,"調教場所"] = "札幌"
    df.loc[df["調教コース"].str.contains("(小)")==True,"調教場所"] = "小倉"
    df.loc[df["調教コース"].str.contains("(門)")==True,"調教場所"] = "門別"
    df.loc[df["調教コース"].str.contains("(新)")==True,"調教場所"] = "新潟"
    df.loc[df["調教コース"].str.contains("(京)")==True,"調教場所"] = "京"
    df.loc[df["調教コース"].str.contains("(東)")==True,"調教場所"] = "東京"
    df.loc[df["調教コース"].str.contains("(阪)")==True,"調教場所"] = "阪神"

    df["坂路調教"] = df["調教コース"].str.contains("(坂)")
    df["調教の馬場"] = df["調教の馬場"].str.replace("稍","稍重")
    df["調教の馬場"] = df["調教の馬場"].str.replace("不","不良")

    return df

def cleanRaceWrapper(i_filepath,o_filepath):
 
    df = clean.cleanSpaceAndLoad(i_filepath,o_filepath)
    df = cleanRaceData(df)    
    df.to_csv(o_filepath,index=False)

def cleanHorseWrapper(i_filepath,o_filepath):

    df = clean.cleanSpaceAndLoad(i_filepath,o_filepath)
    df = cleanHorseData(df)    
    df.to_csv(o_filepath,index=False)

def cleanTrainWrapper(i_filepath,o_filepath):

    df = cleanTrainData(df)    
    df.to_csv(o_filepath,index=False)

