import pandas as pd

def calc(df):

    df["勝"] = 0

    df.loc[df["地方"]!=1,"勝"] = df["勝"] + 5
    df.loc[df["性別"]!="牝","勝"] = df["勝"] + 1
    df.loc[df["所属"]=="栗東","勝"] = df["勝"] + 1
    df.loc[(df["開催"]=="福島") & (df["所属"]=="栗東"),"勝"] = df["勝"] + 1

    df.loc[df["国際"]==1,"勝"] = df["勝"] + 1

    df.loc[df["1前馬場"]=="稍重","勝"] = df["勝"] + 1
    df.loc[df["1前馬場"]=="重","勝"] = df["勝"] + 1
    df.loc[df["1前不利"]==True,"勝"] = df["勝"] + 1
    df.loc[(df["1前開催"]!="中山"),"勝"] = df["勝"] + 1
    df.loc[(df["1前開催"]=="京都"),"勝"] = df["勝"] + 1

    df.loc[(df["馬体重の差分"]>10),"勝"] = df["勝"] + 1
    df.loc[(df["馬体重の差分"]>-10),"勝"] = df["勝"] + 1
    df.loc[(df["馬体重"] >= 450),"勝"] = df["勝"] + 1
    df.loc[(df["馬体重"] > 500),"勝"] = df["勝"] + 1

    df.loc[(df["騎手"]=="池添謙一"),"勝"] = df["勝"] + 1
    df.loc[(df["騎手"]!="和田竜二"),"勝"] = df["勝"] + 1
    
    df.loc[(df["年齢"]<=5),"勝"] = df["勝"] + 1
    df.loc[(df["年齢"]==2),"勝"] = df["勝"] + 1
    df.loc[(df["日付-生年月日"]<365*2.5),"勝"] = df["勝"] + 1

    df.loc[(df["馬名_出走回数"]>=5) & (df["馬名_出走回数"]<=7),"勝"] = df["勝"] + 1
    df.loc[(df["馬名_騎手_出走回数"] >= 5),"勝"] = df["勝"] + 1
    
    df.loc[(df["平均オッズ"]<50),"勝"] = df["勝"] + 3
    df.loc[(df["1前レース間隔"]>10),"勝"] = df["勝"] + 1
    df.loc[(df["斤量/馬体重"]<0.11),"勝"] = df["勝"] + 1
    df.loc[(df["1前頭数"] > df["頭数"]),"勝"] = df["勝"] + 1
    df.loc[(df["馬名_勝数"]==1) & (df["レース条件"] != "1勝"),"勝"] = df["勝"] + 3
    df.loc[(df["馬名_開催_出走回数"] < 5),"勝"] = df["勝"] + 1

    return df
