
import pandas as pd
import lightgbm as lgb

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

df = pd.read_csv("sample_horse.csv")
df = df[~(df["レース名"] == "第64回有馬記念(G1)")]
df = df[~(df["着順"] == "取")]
df = df[~(df["着順"] == "中")]
df = df[~(df["着順"] == "除")] 

horse = LabelEncoder()
horse = horse.fit(df["馬名"])
df["馬名_L"] = horse.transform(df["馬名"])

race = LabelEncoder()
race = race.fit(df["レース名"])
df["レース名_L"] = race.transform(df["レース名"])


valid = df[df["レース名"] == "第60回宝塚記念(G1)"]
train = df[~(df["レース名"] == "第60回宝塚記念(G1)")]

query = train.groupby("レース名_L").count()
query_v = valid.groupby("レース名_L").count()

lgtrain = lgb.Dataset(train[["馬名_L"]].values, train["着順"].values, categorical_feature=[0],group=query["馬名"])
lgvalid = lgb.Dataset(valid[["馬名_L"]].values, valid["着順"].values, categorical_feature=[0],group=query_v["馬名"])

label_gain = []

for i in range(0,20):
	label_gain.append(2^i -1)

max_position = 20
lgbm_params =  {
	'task': 'train',
	'boosting_type': 'gbdt',
	'objective': 'lambdarank',
	'metric': 'ndcg',   # for lambdarank
	'ndcg_eval_at': list(range(1,max_position)),  # for lambdarank
	'max_position': max_position,  # for lambdarank
	'learning_rate': 0.05,
	'min_data': 1,
	'min_data_in_bin': 1,
	'label_gain' : label_gain
}

lgb_clf = lgb.train(
	lgbm_params,
	lgtrain,
	categorical_feature=[0,1],
	num_boost_round=100,
	valid_sets=[lgtrain, lgvalid],
	valid_names=['train','valid'],
	verbose_eval=1
)

target = pd.read_csv("targetHorseList.csv")
target["馬名_L"] = horse.transform(target["馬名"])

y_predict = lgb_clf.predict(target[["馬名_L"]].values)
target["score"] = y_predict
target["rank"] = target.rank(method="min")["score"]
target[["rank","馬名","score"]].sort_values("score").to_csv("predict.csv")

