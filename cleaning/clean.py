import pandas as pd
import numpy as np

def dropFeatures(df,feature_list):    
    for feature in feature_list:
        df.drop(feature,axis=1,inplace=True)
    return df

def cleanSpaceAndLoad(i_filepath,o_filepath):

    with open(i_filepath,encoding="utf-8") as f:
        filedata = f.read()
        filedata = filedata.replace(" ","")
        filedata = filedata.replace(" ","")

        with open(o_filepath,"w",encoding="utf-8") as fout:
            fout.write(filedata)

    df = pd.read_csv(o_filepath)

    return df

def cleanRank(df):

    df["着順"] = df["着順"].astype("str")
    df["着順"] = df["着順"].str.replace("中","nan")
    df["着順"] = df["着順"].str.replace("取","nan")
    df["着順"] = df["着順"].str.replace("除","nan")
    df["着順"] = df["着順"].str.replace("失","nan")
    df["着順"] = df["着順"].str.replace("10\(降\)","nan")
    df["着順"] = df["着順"].str.replace("11\(降\)","nan")
    df["着順"] = df["着順"].str.replace("12\(降\)","nan")
    df["着順"] = df["着順"].str.replace("13\(降\)","nan")
    df["着順"] = df["着順"].str.replace("14\(降\)","nan")
    df["着順"] = df["着順"].str.replace("15\(降\)","nan")
    df["着順"] = df["着順"].str.replace("16\(降\)","nan")
    df["着順"] = df["着順"].str.replace("2\(降\)","nan")
    df["着順"] = df["着順"].str.replace("3\(降\)","nan")
    df["着順"] = df["着順"].str.replace("4\(降\)","nan")
    df["着順"] = df["着順"].str.replace("5\(降\)","nan")
    df["着順"] = df["着順"].str.replace("6\(降\)","nan")
    df["着順"] = df["着順"].str.replace("7\(降\)","nan")
    df["着順"] = df["着順"].str.replace("8\(降\)","nan")
    df["着順"] = df["着順"].str.replace("9\(降\)","nan")

    df["着順"] = df["着順"].astype("float")
    return df

def cleanHorseWeight(df):
    
    df["馬体重の差分"] = df["馬体重"].str.split("(",expand=True)[1].str.replace(")","")
    df["馬体重"] = df["馬体重"].str.split("(",expand=True)[0]
    df["馬体重"] = df["馬体重"].str.replace("計不","")
    
    return df

def cleanCornerRank(df):

    df["コーナー数"] = df["通過"].str.split("-",expand=True).count(axis=1)
    df["スタート順位"] = df["通過"].str.split("-",expand=True)[0]

    if df["コーナー数"].max() == 3:
        df["通過1"] = df["通過"].str.split("-",expand=True)[0]
        df["通過2"] = df["通過"].str.split("-",expand=True)[1]
        df["通過3"] = df["通過"].str.split("-",expand=True)[2]
    elif df["コーナー数"].max() == 2:
        df["通過1"] = df["通過"].str.split("-",expand=True)[0]
        df["通過2"] = df["通過"].str.split("-",expand=True)[1]
    elif df["コーナー数"].max() == 1:
        df["通過1"] = df["通過"].str.split("-",expand=True)[0]
    else:
        df["通過1"] = df["通過"].str.split("-",expand=True)[0]
        df["通過2"] = df["通過"].str.split("-",expand=True)[1]
        df["通過3"] = df["通過"].str.split("-",expand=True)[2]
        df["通過4"] = df["通過"].str.split("-",expand=True)[3]

    df.loc[(df["コーナー数"]==1),"通過4"] = df["通過1"]
    df.loc[df["コーナー数"]==1,"通過1"] = np.nan

    df.loc[df["コーナー数"]==2,"通過4"] = df["通過2"]
    df.loc[df["コーナー数"]==2,"通過3"] = df["通過1"]
    df.loc[df["コーナー数"]==2,"通過2"] = np.nan
    df.loc[df["コーナー数"]==2,"通過1"] = np.nan

    df.loc[df["コーナー数"]==3,"通過4"] = df["通過3"]
    df.loc[df["コーナー数"]==3,"通過3"] = df["通過2"]
    df.loc[df["コーナー数"]==3,"通過2"] = df["通過1"]
    df.loc[df["コーナー数"]==3,"通過1"] = np.nan

    df["通過1"] = df["通過1"].astype("float")
    df["通過2"] = df["通過2"].astype("float")
    df["通過3"] = df["通過3"].astype("float")
    df["通過4"] = df["通過4"].astype("float")

    return df

def cleanTime(df):

    df["タイム"] = df["タイム"].str.replace(".",":") 
    df["タイム"] = df["タイム"].str.strip("\xa0") 
    df["タイム"]  = pd.to_datetime(df["タイム"],format="%M:%S:%f")
    df["タイム(秒)"]  = df["タイム"].dt.minute * 60 + df["タイム"].dt.second + df["タイム"].dt.microsecond / 1000000

    return df

def cleanHorseName(df):

    df["馬名"] = df["馬名"].str.replace("□","")
    df["馬名"] = df["馬名"].str.replace("○","")
    df["馬名"] = df["馬名"].str.replace("地","")
    df["馬名"] = df["馬名"].str.replace("外","")

    df["馬名"] = df["馬名"].str.replace("　","")
    df["馬名"] = df["馬名"].str.replace(" ","")

    df["馬名_spare"] = df["馬名"]
    df["馬名"] = df["馬名"].str.replace(r"([a-z])","")
    df["馬名"] = df["馬名"].str.replace(r"([A-Z])","")
    df.loc[df["馬名"]=="","馬名"] = df["馬名_spare"]
    df.drop("馬名_spare",axis=1,inplace=True)

    return df 

def cleanRemarks(df):

    df["出遅れ"] = df["備考"].str.contains("(出遅れ|出脚鈍い)")
    df["不利"] = df["備考"].str.contains("(不利)")
    df["出遅れ"] = df["出遅れ"].fillna(False)
    df["不利"] = df["不利"].fillna(False)

    return df

def cleanRewards(df):
    df["賞金"] = df["賞金"].astype(str).str.replace(",","")
    return df

def cleanHeld(df):

    df["開催回数"] = df["開催"].str.extract("(^[0-9]+)")
    df["開催日数"] = df["開催"].str.extract("([0-9]+$)")

    for i in range(0,10):
        df["開催"] = df["開催"].str.replace(str(i),"")

    return df

def cleanCourseDist(df):

    df["コースの種類"] = df["距離"].str[:1]
    df["距離"] = df["距離"].str.extract(r"([0-9][0-9]+)")
    df["距離"] = df["距離"].astype("int")

    return df

def cleanBaba(df):

    df["馬場"] = df["馬場"].str.replace("稍","稍重")
    df["馬場"] = df["馬場"].str.replace("不","不良")
    df["馬場"] = df["馬場"].str.replace("ダート","")

    return df

def cleanPace(df):

    df["ペース(前半)"] = df["ペース"].str.split("-",expand=True)[0]
    df["ペース(後半)"] = df["ペース"].str.split("-",expand=True)[1]

    return df

