def makeList():

    num_features = [
        "馬体重",
        "馬体重の差分",
        "枠番",
        "馬番",

        "馬体重の差分/馬体重",
        "斤量/馬体重",
        "(馬体重+斤量)-1前",
        
        "馬体重 * 距離",
        "斤量 * 距離",
        "馬体重の差分 * 距離",
        "斤量/馬体重 * 距離",
        "距離/1前 * 馬体重の差分/馬体重",
        "開催日数/枠番",
        "開催日数*枠番",
        "開催日数*枠番+R",
        "開催日数*枠番*R",

        "獲得賞金3",
        "獲得賞金5",

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
    num_features.extend(makeLastPerNow())
    num_features.extend(makePrevAvg())

    return num_features

def makeLastPerNow():
    lst = []
    num_categories = [
        "馬体重","馬体重の差分","斤量","頭数","枠番","R","距離",
    ]
    for num_category in num_categories:
        lst.append(num_category+"/1前")
        lst.append(num_category+"-1前")
    return lst

def makePrevRun():

    num_categories = [
        "賞金",         "タイム(秒)",       "上り", 
        "馬体重",       "斤量",     "馬体重の差分",  "ペース(前半)",     "ペース(後半)",
        "距離",         "頭数",     "枠番",         "R",                "ﾀｲﾑ指数",
        "馬場指数",     
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

def makePrevAvg():

    lst = []
    prefix = "平均"    
    num_categories = [
        # レース前に分かるもの
        "馬体重",       "斤量",     "馬体重の差分",  "頭数",             "枠番",
        "R",            "距離",     

        # レース前に分からないもの
        "賞金",         
        "ﾀｲﾑ指数",      "馬場指数",
    ]

    for num_category in num_categories:
        lst.append(prefix+num_category)
    
    return lst


def makePrevCount():

    prefix = "馬名_"    
    str_categories = [
        "開催",     "馬場",     "レース条件",   
        "距離カテゴリ", "コースの種類",     "騎手"
    ]

    # 着順から作成したもの
    lst = [
        prefix+"勝数",
        prefix+"連対数",
        prefix+"複勝数",
        prefix+"2着数",
        prefix+"3着数",
        prefix+"出走回数"
    ]
    for str_category in str_categories:
        lst.append(prefix+str_category+"_出走回数")

    return lst

def makeDimCount(category_name):

    prefix = category_name+"_昨年"    
    lst = [
        prefix+"勝数",
        prefix+"連対数",
        prefix+"複勝数",
        prefix+"2着数",
        prefix+"3着数",
        prefix+"出走回数"
    ]
    return lst


def makeDimAverage(category_name):
    num_categories = [
        "賞金",        
        "ﾀｲﾑ指数",      
    ]
    lst = []
    prefix = category_name+"_昨年平均"    
    for num_category in num_categories:
        lst.append(prefix + num_category)

    return lst
