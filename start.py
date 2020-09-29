
from molding import molding
from featureEngineering import horseHistory
from featureEngineering import calcFeatures
from cleaning import cleanWrapper

from model import PredictionModel
from features import numFeature
from features import categoryFeature

# cleanWrapper.cleanRaceWrapper("crowling/result/raceTable.csv","cleaning/result/raceTable.csv")
# cleanWrapper.cleanHorseWrapper("crowling/result/horseTable.csv","cleaning/result/horseTable.csv")

# horseHistory.read("cleaning/result/horseTable.csv","featureEngineering/result/horseTable_hist.csv")
# calcFeatures.read("featureEngineering/result/horseTable_hist.csv","cleaning/result/raceTable.csv","featureEngineering/result/joinTable.csv")
# molding.molding("featureEngineering/result/joinTable.csv"

train_data_paths = [
    "dataset/train1.csv",
    "dataset/train2.csv"
]
valid_data_path = "dataset/valid.csv"
valid_query_path = "dataset/valid_query.csv"

model = PredictionModel.PredictionModel()
model.setNumFeatures(numFeature.makeList())
model.setStrFeatures(categoryFeature.makeList())
model.loadTrainData(train_data_paths)
model.loadValidData(valid_data_path,valid_query_path)
model.predict()