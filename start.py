
import pandas as pd
import glob 

from molding.molding4 import molding
from featureEngineering import horseHistory
from featureEngineering import horseAgg
from featureEngineering import calcFeatures
from featureEngineering import categoryAgg
from cleaning import cleanWrapper

from predict import PredictionModel
# from model.reg_timeindex import numFeature
# from model.reg_timeindex import categoryFeature
from model.oishisa_zenjitsu_cross import numFeature
from model.oishisa_zenjitsu_cross import categoryFeature

# from model.blood import numFeature
# from model.blood import categoryFeature

from calcReturn import single

from predict import RuleModel

import makeTarget

def clean():
    cleanWrapper.cleanRaceWrapper("crowling/result/raceTable.csv","cleaning/result/raceTable.csv")
    cleanWrapper.cleanHorseWrapper("crowling/result/horseTable.csv","cleaning/result/horseTable.csv")

def calcFeature():
    # horseHistory.read("cleaning/result/horseTable.csv","featureEngineering/result/horseTable_hist.csv")
    # horseAgg.read("featureEngineering/result/horseTable_hist.csv","featureEngineering/result/horseTable_hist2.csv")
    # categoryAgg.read("cleaning/result/raceTable.csv","featureEngineering/result/raceTable.csv")
    # categoryAgg.read("featureEngineering/result/raceTable.csv","featureEngineering/result/raceTable.csv")
    calcFeatures.read("featureEngineering/result/horseTable_hist2.csv","featureEngineering/result/raceTable.csv","featureEngineering/result/joinTable.csv")

def mold():
    molding("featureEngineering/result/joinTable.csv","molding/bloodTable.csv")

def predict():

    train_data_paths = [
            "dataset/train1.csv",
            "dataset/train2.csv",
            "dataset/train3.csv",
            "dataset/train4.csv",
    ]

    valid_data_path = "dataset/valid.csv"
    valid_query_path = "dataset/valid_query.csv"

    model = PredictionModel.PredictionModel()
    model.setNumFeatures(numFeature.makeList())
    model.setStrFeatures(categoryFeature.makeList())
    model.loadTrainData(train_data_paths)
    model.loadValidData(valid_data_path,valid_query_path)
    # model.train("30倍以下")
    # model.predict()
    model.train("1着率")
    model.predict()
    # model.train("勝")
    # model.predict()    
    model.writeData()

def valid_oishisa():

    df = pd.read_csv("result/predict.csv")
    single.calcSingle(df)

    df["回収"] = 0
    df.loc[df["着順"]==1,"回収"]=df["単勝"]

    cutoff_border = 30

    race_count = df[(df["単勝"]<=cutoff_border) & (df["rank"]==1)]["回収"].count()
    vote_count = df[(df["単勝"]<=cutoff_border) & (df["rank_dup"]==1)]["回収"].count()
    hit_count = df[(df["着順"]==1) & (df["rank"]==1)]["回収"].count()
    vote_hit_count = df[(df["着順"]==1) & (df["rank_dup"]==1)]["回収"].count()

    print(str(cutoff_border)+"倍以下 的中：\t"+str(vote_hit_count / vote_count))
    print(str(cutoff_border)+"倍以下 回収：\t"+str(df[(df["単勝"]<=cutoff_border) & (df["rank_dup"]==1)]["回収"].mean()))
    print(str(cutoff_border)+"倍以下 件数：\t"+str(df[(df["単勝"]<=cutoff_border) & (df["rank_dup"]==1)]["回収"].count()))

    print(str(cutoff_border)+"倍以下 的中：\t"+str(hit_count / race_count))
    print(str(cutoff_border)+"倍以下 回収：\t"+str(df[(df["単勝"]<=cutoff_border) & (df["rank"]==1)]["回収"].mean()))
    print(str(cutoff_border)+"倍以下 件数：\t"+str(race_count))

def valid():

    df = pd.read_csv("result/predict.csv")
    single.calcSingle(df)

    df["回収"] = 0
    df.loc[df["着順"]==1,"回収"]=df["単勝"]

    cutoff_border = 30

    race_count = df[(df["単勝"]<=cutoff_border) & (df["rank"]==1)]["回収"].count()
    hit_count = df[(df["単勝"]<=cutoff_border) & (df["着順"]==1) & (df["rank"]==1)]["回収"].count()

    print(str(cutoff_border)+"倍以下 的中：\t"+str(hit_count / race_count))
    print(str(cutoff_border)+"倍以下 回収：\t"+str(df[(df["単勝"]<=cutoff_border) & (df["rank"]==1)]["回収"].mean()))
    print(str(cutoff_border)+"倍以下 件数：\t"+str(race_count))

def predictTarget(urls,year,month,day):

    target_paths = []
    train_data_paths = [
            "dataset/train1.csv",
            "dataset/train2.csv",
            "dataset/train3.csv",
            "dataset/train4.csv",
    ]

    maketarget = makeTarget.makeTarget()
    maketarget.getSession()

    model = PredictionModel.PredictionModel()
    model.setNumFeatures(numFeature.makeList())
    model.setStrFeatures(categoryFeature.makeList())
    model.loadTrainData(train_data_paths)

    for u in urls:
        maketarget.setRaceUrl(u)
        maketarget.exec(year,month,day)
        target_paths.append(maketarget.getFilePath())

    for target_path in target_paths:
        print(target_path)
        model.loadTargetData(target_path)
        model.setResultPath(target_path.replace("target","result"))
        model.train("勝")
        model.predictTarget()
        ruleTarget(target_path)


def ruleTarget(target_path):
    df = pd.read_csv(target_path)
    df_query = [len(df)]
    RuleModel.calcRank(df,df_query,target_path.replace("target","oishisa"))

def oishisa():
    df = pd.read_csv("dataset/valid.csv")
    df_query = pd.read_csv("dataset/valid_query.csv")["レース"]
    RuleModel.calcRank(df,df_query,"result/predict.csv")

def main():
    

    urls = [    
        # "https://race.netkeiba.com/race/shutuba.html?race_id=202005050701",
        # "https://race.netkeiba.com/race/shutuba.html?race_id=202009050701",

        # "https://race.netkeiba.com/race/shutuba.html?race_id=202005050702",
        # "https://race.netkeiba.com/race/shutuba.html?race_id=202009050702",

        # "https://race.netkeiba.com/race/shutuba.html?race_id=202005050703",
        # "https://race.netkeiba.com/race/shutuba.html?race_id=202009050703",

        # "https://race.netkeiba.com/race/shutuba.html?race_id=202005050704",

        # "https://race.netkeiba.com/race/shutuba.html?race_id=202009050707",

        # "https://race.netkeiba.com/race/shutuba.html?race_id=202005050708",
        # "https://race.netkeiba.com/race/shutuba.html?race_id=202009050708",

        # "https://race.netkeiba.com/race/shutuba.html?race_id=202005050709",
        # "https://race.netkeiba.com/race/shutuba.html?race_id=202009050709",

        # "https://race.netkeiba.com/race/shutuba.html?race_id=202005050710",
        # "https://race.netkeiba.com/race/shutuba.html?race_id=202009050710",

        # "https://race.netkeiba.com/race/shutuba.html?race_id=202005050711",
        # "https://race.netkeiba.com/race/shutuba.html?race_id=202009050711",

        "https://race.netkeiba.com/race/shutuba.html?race_id=202005050912",
        # "https://race.netkeiba.com/race/shutuba.html?race_id=202009050712",

    ]


    # clean()
    # calcFeature()
    # mold()

    predictTarget(urls,2020,11,29)
    # predict()
    # valid()
    # oishisa()

main()