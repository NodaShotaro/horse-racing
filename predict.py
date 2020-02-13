
import pandas as pd
import lightgbm as lgb
import math

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def smoothing(cnt,score,average_score,alpha=0.1):
	return (1-(math.e)**((-alpha)*cnt)) * score + ((math.e)**((-alpha)*cnt)) * average_score

# データセットの整形・欠損対策
df = pd.read_csv("sample_horse.csv")
df = df[~(df["レース名"] == "第64回有馬記念(G1)")]
df = df[~(df["着順"] == "取")]
df = df[~(df["着順"] == "中")]
df = df[~(df["着順"] == "除")] 

df["レース"] = df["日付"] + "-" + df["ラウンド数"]
df["日付"] = pd.to_datetime(df["日付"])
df["年"] = df["日付"].dt.year

# カテゴリ属性のラベリング
horse = LabelEncoder()
horse = horse.fit(df["馬名"])
df["馬名_L"] = horse.transform(df["馬名"])

jockey = LabelEncoder()
jockey = jockey.fit(df["騎手"])
df["騎手_L"] = jockey.transform(df["騎手"])

weather = LabelEncoder()
weather = weather.fit(df["天候"])
df["天候_L"] = weather.transform(df["天候"])

land = LabelEncoder()
land = land.fit(df["地面"])
df["地面_L"] = land.transform(df["地面"])

place = LabelEncoder()
place = place.fit(df["場所"])
df["場所_L"] = place.transform(df["場所"])

race = LabelEncoder()
race = race.fit(df["レース"])
df["レース_L"] = race.transform(df["レース"])

valid = df[(df["日付"].dt.year == 2019)]
train = df[~(df["日付"].dt.year == 2019)]

query = []
lst = pd.DataFrame()
for i,t in train.groupby("レース_L"):
	query.append(t["レース_L"].count())
	lst = pd.concat([lst,t])

train = lst

query_v = []
tmp_lst = pd.DataFrame()
for i,t in valid.groupby("レース_L"):
	query_v.append(t["レース_L"].count())
	tmp_lst = pd.concat([tmp_lst,t])

valid = tmp_lst

lgtrain = lgb.Dataset(train[["馬名_L","騎手_L","天候_L","地面_L","場所_L","年","3平均着順","馬体重"]].values, train["着順"].values, categorical_feature=[0,1,2,3,4,5],group=query)
lgvalid = lgb.Dataset(valid[["馬名_L","騎手_L","天候_L","地面_L","場所_L","年","3平均着順","馬体重"]].values, valid["着順"].values, categorical_feature=[0,1,2,3,4,5],group=query_v)

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
	'learning_rate': 0.1,
	'min_data': 1,
	'min_data_in_bin': 1,
	'label_gain' : label_gain
}

lgb_clf = lgb.train(
	lgbm_params,
	lgtrain,
	categorical_feature=[0,1,2,3,4,5,6],
	num_boost_round=101,
	valid_sets=[lgtrain, lgvalid],
	valid_names=['train','valid'],
	verbose_eval=1
)

target = pd.read_csv("targetHorseList.csv")
target["天候"] = "曇\xa0"
target["地面"] = "良\xa0"
target["場所"] = "中山"
target["年"] = 2019

target["馬名_L"] = horse.transform(target["馬名"])
target["騎手_L"] = jockey.transform(target["騎手"])
target["天候_L"] = weather.transform(target["天候"])
target["地面_L"] = land.transform(target["地面"])
target["場所_L"] = place.transform(target["場所"])

y_predict = lgb_clf.predict(target[["馬名_L","騎手_L","天候_L","地面_L","場所_L","年","3平均着順","馬体重"]].values)
target["score"] = y_predict
target["rank"] = target.rank(method="min")["score"]
target[["rank","馬名","score"]].sort_values("score").to_csv("predict.csv",index=False)

print(valid["レース_L"].count())
print(train["レース_L"].count())
