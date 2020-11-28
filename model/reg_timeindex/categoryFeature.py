
def makeList():

    category_features = [
        "枠番",
        "馬番",
        "年齢",
        "性別",
        "地方",
        "国際",
        "所属",
        "毛色",

        "コース*距離",
        "コース*枠番",        
        "所属*開催",
        "所属*距離カテゴリ",
        "馬番奇数",
    ]
    category_features.extend(makePrevRun())
    category_features.extend(makeWinRun())
    category_features.extend(makePlaceRun())
    category_features.extend(makeSameCondLast())
    return category_features

def makeSameCondLast():
    lst = []
    str_categories = [
        "開催",
        "レース条件",
        "距離カテゴリ",
        "コースの種類",
        "騎手"
    ]
    for str_category in str_categories:
        lst.append("=1前"+str_category)
    return lst


def makePrevRun():

    str_categories = [
        "開催",     "馬場",     "天気",     "レース条件",   
        "出遅れ",   "不利",     "距離カテゴリ", "コースの種類",
    ]
    lst = []
    for i in range(1,6):
        prefix = str(i)+"前"
        for str_category in str_categories:
            lst.append(prefix+str_category)            

    return lst

def makeWinRun():

    str_categories = ["馬場","距離カテゴリ","レース条件","開催"]
    prefix = "1前_勝利時の"

    lst = []
    for str_category in str_categories:
        lst.append(prefix+str_category)
    return lst

def makePlaceRun():
    lst = []
    str_categories = ["馬場","距離カテゴリ","レース条件","開催"]
    for pre_pos in range(0,3):
        prefix = str(pre_pos+1)+"前_複勝時の"
        for str_category in str_categories:
            lst.append(prefix + str_category)
    return lst