def makeList():

    num_features = [
        "馬体重",
        "馬体重の差分",
        "枠番",
        "馬番",

        "距離/1前距離",
        "馬体重の差分/馬体重",
        "距離/1前距離 * 馬体重の差分/馬体重",

        "2前との馬体重の差分",
        "3前との馬体重の差分",

        "馬体重/2前馬体重",
        "馬体重/3前馬体重",
        "斤量/馬体重",
        "斤量差分",
        "馬体重+斤量の差分",
        "馬体重+斤量の割合",

        "馬体重 * 距離",
        "斤量 * 距離",
        "斤量/馬体重 * 距離",

        "獲得賞金3",
        "獲得賞金5",

        # "5走最高着差",
        # "5走最低着差",
        "5走最大ﾀｲﾑ指数",
        "5走最低ﾀｲﾑ指数",
        "5走最速上り",

        "1前_勝利時との斤量差分",
        "1前_勝利時との馬体重の差分",
        "1前_勝利時からの間隔",
        "1前_複勝時との斤量差分",
        "1前_複勝時との馬体重の差分",
        "1前_複勝時からの間隔",
        "日付-生年月日",
    ]

    sex_category = ["牝","牡","セ"]
    for i in range(1,4):
        for sex in sex_category:
            num_features.append(sex + "_"+str(i)+"前レース間隔")

    num_features.extend(makePrevRun())
    num_features.extend(makeWinRun())
    num_features.extend(makePlaceRun())
    return num_features

def makePrevRun():

    num_categories = [
        "着順",         "着差",     "賞金",         "タイム(秒)",       "上り", 
        "スタート順位",  "通過1",    "通過2",        "通過3",            "通過4",
        "馬体重",       "斤量",     "馬体重の差分",  "ペース(前半)",     "ペース(後半)",
        "距離",         "頭数",             "枠番",
        "R",            "ﾀｲﾑ指数"
    ]

    lst = []
    for i in range(1,6):
        prefix = str(i)+"前"
        for num_category in num_categories:
            lst.append(prefix+num_category)

    for i in range(1,5):
        prefix = str(i)+"前"
        lst.append(str(i) + "前レース間隔")

    return lst

def makeWinRun():

    num_categories = ["斤量","馬体重","ﾀｲﾑ指数"]
    prefix = "1前_勝利時の"

    lst = []
    for num_category in num_categories:
        lst.append(prefix+num_category)
    return lst

def makePlaceRun():
    lst = []
    num_categories = ["斤量","馬体重","ﾀｲﾑ指数"]
    for pre_pos in range(0,3):
        prefix = str(pre_pos+1)+"前_複勝時の"
        for num_category in num_categories:
            lst.append(prefix + num_category)
    return lst