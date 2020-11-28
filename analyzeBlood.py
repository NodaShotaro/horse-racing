
import pandas as pd

def makePrefix(length):
    candidates = ["父","母"]
    prefix_list = ["父","母"]
    tmp = []

    for i in range(0,length-1):
        for prefix in prefix_list:
            for candidate in candidates:
                tmp.append(prefix+candidate)
        prefix_list = tmp
        tmp = []

    return prefix_list

def searchMajorFather(df):

    lst = df["父"].value_counts() * 1/2
    for i in range(1,5):
        prefix_list = makePrefix(i)

        for prefix in prefix_list:
            x = df[prefix+"父"].value_counts() * ((1/2) ** (i+1))
            x = pd.DataFrame(x)
            lst = pd.concat([x,lst],axis=1)

    lst.fillna(0,inplace=True)
    lst["合計"] = lst.sum(axis=1)
    lst.sort_values("合計",inplace=True)
    return lst

def searchMajorSon(df,name):

    lst = df[df["父父"] == name]["父"].value_counts() * 1/2
    lst = pd.DataFrame(lst)
    for i in range(1,4):
        prefix_list = makePrefix(i)
        for prefix in prefix_list:
            print(prefix)
            x = df[df[prefix+"父父"] == name][prefix+"父"].value_counts()* ((1/2) ** (i+1))
            x = pd.DataFrame(x)
            lst = pd.concat([x,lst],axis=1)
        
        lst["合計"] = lst.sum(axis=1)
        lst.sort_values("合計",inplace=True)
    return lst

def searchMajorGrandSon(df,name):

    lst = df[df["父母父"] == name]["父"].value_counts()# * 1/2
    lst = pd.DataFrame(lst)
    for i in range(1,3):
        prefix_list = makePrefix(i)
        for prefix in prefix_list:
            print(prefix)
            x = df[df[prefix+"父母父"] == name][prefix+"父"].value_counts()#* ((1/2) ** (i+1))
            x = pd.DataFrame(x)
            lst = pd.concat([x,lst],axis=1)
        
        lst["合計"] = lst.sum(axis=1)
        lst.sort_values("合計",inplace=True)
    return lst

def calcBloodRate(df,blood_name):

    df[blood_name] = 0
    blood_rate = 1

    for i in range(1,6):
        prefix_list = makePrefix(i)
        for prefix in prefix_list:
            df.loc[df[prefix]==blood_name,blood_name] = df[blood_name] + blood_rate * ((1/2)**(i))
    
    return df

def normalizeName(df):

    for i in range(1,6):
        prefix_list = makePrefix(i)
        for prefix in prefix_list:
        
            # (米)などを抽出して別の列へ展開
            df[prefix+"_系列"] = df[prefix].str.extract(r'(\(.*\))')
            df[prefix] = df[prefix].str.split(r'(\()',expand=True)[0]

            # カタカナと英語が混在する名前をカタカナで統一
            df[prefix].fillna("",inplace=True)
            df.loc[df[prefix].str.contains(r"([ア-ン|ー][A-z])"),prefix] = df[prefix].str.replace(r'([(A-z| |\')])',"")
    
    return df

# blood_sum 値以上の血に対して特徴量を生成
# blood_sum = 5のとき：
#・サンプル内にその産駒が10頭存在する場合
#・サンプル内にBMS関係にある馬が20頭存在する場合など
def calcMajorBlood(df,blood_sum):

    major_blood_list = searchMajorFather(df)["合計"]
    major_blood_list = list(major_blood_list[major_blood_list>blood_sum].index)

    cnt = 1
    end = len(major_blood_list)

    for major_blood in major_blood_list:

        print(str(cnt) + "/" + str(end))
        df = calcBloodRate(df,major_blood)
        cnt = cnt + 1

    return df


# import pandas as pd
# from cleaning import clean
# import analyzeBlood as aB
# df = pd.read_csv("crowling/result/bloodTable.csv")
# df = aB.normalizeName(df)
# df = aB.calcMajorBlood(df,5)
# df = clean.cleanHorseName(df)
