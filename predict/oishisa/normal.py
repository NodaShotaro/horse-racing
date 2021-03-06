import pandas as pd


def calc(df):
    df["勝"] = 0

    df.loc[df["地方"]!=1,"勝"] = df["勝"] + 5
    df.loc[df["所属"]=="栗東","勝"] = df["勝"] + 1

    df.loc[df["国際"]==1,"勝"] = df["勝"] + 1
    df.loc[df["性別"]!="牝","勝"] = df["勝"] + 1
    df.loc[df["馬番奇数"]==False,"勝"] = df["勝"] + 1

#    df.loc[df["1前馬場"]=="良","勝"] = df["勝"] + 1
    df.loc[df["1前不利"]==True,"勝"] = df["勝"] + 1
    df.loc[(df["1前着差"]<=0.0) & (df["1前着順"]!=1),"勝"] = df["勝"] + 1
    df.loc[(df["1前着順"]!=1),"勝"] = df["勝"] + 1
    df.loc[(df["1前着差"]<2.0),"勝"] = df["勝"] + 3
    df.loc[(df["2前着差"]<2.0),"勝"] = df["勝"] + 3

    df.loc[(df["平均オッズ"]<50),"勝"] = df["勝"] + 1
    df.loc[(df["1前オッズ"]>2),"勝"] = df["勝"] + 1

    df.loc[(df["1前開催"]!="中山"),"勝"] = df["勝"] + 1
    df.loc[(df["1前開催"]=="京都"),"勝"] = df["勝"] + 1
    df.loc[(df["開催"]=="中山") & (df["所属"]=="栗東"),"勝"] = df["勝"] + 1
    df.loc[(df["開催"]=="福島") & (df["所属"]=="栗東"),"勝"] = df["勝"] + 1

    df.loc[(df["1前レース間隔"]>90),"勝"] = df["勝"] + 1
    df.loc[(df["1前レース間隔"]>10),"勝"] = df["勝"] + 3

    df.loc[(df["馬体重"] > 500),"勝"] = df["勝"] + 1
    df.loc[(df["馬体重"] > 450),"勝"] = df["勝"] + 1

    df.loc[(df["馬体重の差分"]>10),"勝"] = df["勝"] + 1
#    df.loc[(df["馬体重の差分"]>14),"勝"] = df["勝"] + 1
    df.loc[(df["馬体重の差分"]>-10),"勝"] = df["勝"] + 1
    df.loc[(df["斤量/馬体重"]<0.11),"勝"] = df["勝"] + 1

    df.loc[(df["距離/1前"]<=1),"勝"] = df["勝"] + 1
    df.loc[(df["1前頭数"] > df["頭数"]),"勝"] = df["勝"] + 1
    df.loc[(df["1前ペース(前半)"] >= df["1前ペース(後半)"]),"勝"] = df["勝"] + 1

    # 騎手・調教師
    df.loc[(df["騎手"]=="池添謙一"),"勝"] = df["勝"] + 1
    df.loc[(df["騎手"]!="和田竜二"),"勝"] = df["勝"] + 1
    df.loc[(df["騎手"]!="岩田康誠"),"勝"] = df["勝"] + 1
    df.loc[(df["騎手"]!="藤田菜七"),"勝"] = df["勝"] + 1

    # レース条件
    df.loc[(df["1前人気"]==1) & (df["レース条件"]=="未勝利"),"勝"] = df["勝"] + 1    

    # 年齢
    df.loc[(df["年齢"]<=5),"勝"] = df["勝"] + 1
    df.loc[(df["年齢"]==2),"勝"] = df["勝"] + 1
    df.loc[(df["日付-生年月日"]<365*2.5),"勝"] = df["勝"] + 1

    # 出走回数
    df.loc[(df["馬名_出走回数"]==1),"勝"] = df["勝"] + 1
    df.loc[(df["馬名_出走回数"]>=5) & (df["馬名_出走回数"]<=7),"勝"] = df["勝"] + 1
    df.loc[(df["馬名_勝数"]==1) & (df["レース条件"] != "1勝"),"勝"] = df["勝"] + 3
    df.loc[(df["馬名_騎手_出走回数"] >= 5),"勝"] = df["勝"] + 1
    df.loc[(df["馬名_開催_出走回数"] < 5),"勝"] = df["勝"] + 1

    df.loc[~((df["馬名_レース条件_出走回数"]>=5) & (df["レース条件"]=="1勝")),"勝"] = df["勝"] + 1
    df.loc[~((df["馬名_レース条件_出走回数"]>=5) & (df["レース条件"]=="2勝")),"勝"] = df["勝"] + 1

    df.loc[(df["馬名_複勝数"] >= 3)&(df["馬名_勝数"] == 0),"勝"] = df["勝"] + 1
    df.loc[(df["斤量-1前"] > 0),"勝"] = df["勝"] + 1

    df.loc[(df["枠番"] <= 3),"勝"] = df["勝"] + 1
    df.loc[(df["枠番"] <= 2) & (df["開催日数"]>2),"勝"] = df["勝"] + 1

    df.loc[df["毛色"]=="青鹿毛","勝"] = df["勝"] + 1
    df.loc[df["1前馬場指数"]>=10,"勝"] = df["勝"] + 1
    
    return df