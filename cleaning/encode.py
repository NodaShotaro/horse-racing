
def raceCond(df):

    df["レース賞金"] = df["レース名"].str.extract("([0-9]+万)")[0].str.extract("([0-9]+)")
    df["レース賞金"].fillna(0,inplace=True)
    df.loc[(df["レース賞金"].astype("int") <= 500) & (df["レース賞金"].astype("int") > 0),"レース条件"] = "1勝"
    df.loc[(df["レース賞金"].astype("int") <= 1000) & (df["レース賞金"].astype("int") > 500),"レース条件"] = "2勝"
    df.loc[df["レース賞金"].astype("int") > 1000,"レース条件"] = "3勝"

    df["buf"] = df["レース名"].str.extract(r"(未勝利)")
    df.loc[df["レース条件"].isnull(),"レース条件"] = df["buf"]

    df["buf"] = df["レース名"].str.extract(r"(新馬)")
    df.loc[df["レース条件"].isnull(),"レース条件"] = df["buf"]

    df["buf"] = df["レース名"].str.extract(r"(1勝)")
    df.loc[df["レース条件"].isnull(),"レース条件"] = df["buf"]

    df["buf"] = df["レース名"].str.extract(r"(2勝)")
    df.loc[df["レース条件"].isnull(),"レース条件"] = df["buf"]

    df["buf"] = df["レース名"].str.extract(r"(G[1-3])")
    df.loc[df["レース条件"].isnull(),"レース条件"] = df["buf"]
    df.loc[df["レース条件"].isnull(),"レース条件"] = "名前付き"

    df["buf"] = df["開催"].str.contains(r"(帯広ば|門別|水沢|浦和|船橋|大井|川崎|金沢|笠松|名古屋|園田|姫路|高知|佐賀)")
    df.loc[df["buf"]==True,"レース条件"] = "地方"
    df.drop("buf",axis=1,inplace=True)
    df.drop("レース賞金",axis=1,inplace=True)

    return df

def courseCategory(df):

    df.loc[(df["コースの種類"]=="芝") & (df["距離"] < 1400),"距離カテゴリ"] = "芝_短距離"
    df.loc[(df["コースの種類"]=="芝") & (df["距離"] >= 1400) & (df["距離"] < 2000),"距離カテゴリ"] = "芝_マイル"
    df.loc[(df["コースの種類"]=="芝") & (df["距離"] >= 2000) & (df["距離"] < 2600),"距離カテゴリ"] = "芝_中距離"
    df.loc[(df["コースの種類"]=="芝") & (df["距離"] >= 2600),"距離カテゴリ"] = "芝_長距離"

    df.loc[(df["コースの種類"]=="ダ") & (df["距離"] < 1400),"距離カテゴリ"] = "ダ_短距離"
    df.loc[(df["コースの種類"]=="ダ") & (df["距離"] >= 1400) & (df["距離"] < 2000),"距離カテゴリ"] = "ダ_マイル"
    df.loc[(df["コースの種類"]=="ダ") & (df["距離"] >= 2000),"距離カテゴリ"] = "ダ_中距離"

    return df

def paceCategory(df):

    df.loc[df["ペース(前半)"] > df["ペース(後半)"],"ペース"] = "ハイペース"
    df.loc[df["ペース(前半)"] <= df["ペース(後半)"],"ペース"] = "ローペース"
    
    return df

def footStyle(df):

    df.loc[(df["通過4"] == 1.0),"展開"] = "逃げ"
    df.loc[(df["通過4"] > 1.0) & (df["通過4"] <= 4.0),"展開"] = "先行"
    df.loc[(df["通過4"] > 4.0) & (df["着順"] < df["通過4"]),"展開"] = "差し"
    df.loc[(df["通過4"] > 4.0) & (df["着順"] >= df["通過4"]),"展開"] = "後位"

    return df