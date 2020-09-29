
import pandas as pd
import lightgbm as lgb
import math
import os
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from . import normalizeDF

class PredictionModel():

	def __init__(self):
		self.normalizer = normalizeDF.normalizeDF()
		self.num_features= []
		self.str_features= []
		self.lgb_clf_list  = []
		self.feature_list  = []
		self.str_feature_index_list = []

	def loadTrainData(self,train_data_paths):
		self.train_data_list = []
		for path in train_data_paths:
			self.train_data_list.append(pd.read_csv(path))

	def loadValidData(self,valid_data_path,valid_query_path):
		self.valid_data = pd.read_csv(valid_data_path)
		self.valid_query = pd.read_csv(valid_query_path)["レース"]

	def setNumFeatures(self,num_features):
		self.num_features= num_features

	def setStrFeatures(self,str_features):
		self.str_features= str_features

	def makeNormalizer(self):
		df = pd.DataFrame()
		df = pd.concat([df,self.valid_data])
		for train_data in self.train_data_list:
			df = pd.concat([train_data,df])
		
		for cf in self.str_features:
			if cf in df.columns:
				self.normalizer.registEncoder(df[cf],cf)
			else:
				self.normalizer.registEncoder(df[cf],cf)

		for nf in self.num_features:
			self.normalizer.register(df[nf],nf)

	def makeFeatureList(self):
		self.feature_list = []
		for cf in self.str_features:
			self.feature_list.append(cf+"_L")
		for nf in self.num_features:
			self.feature_list.append(nf)

		self.str_feature_index_list = range(0,len(self.str_features))

	def normalizeCategories(self,df):
		for cf in self.str_features:
			df[cf+"_L"] = self.normalizer.transform(df[cf],cf)
		return df

	def normalizeNum(self,df):
		for nf in self.num_features:
			df[nf] = self.normalizer.normalize(df[nf],nf)
		return df

	def normalize(self):
		for i in range(0,len(self.train_data_list)):
			self.train_data_list[i] = self.normalizeCategories(self.train_data_list[i])
			self.train_data_list[i] = self.normalizeNum(self.train_data_list[i])

		self.valid_data = self.normalizeCategories(self.valid_data)
		self.valid_data = self.normalizeNum(self.valid_data)
	
	def trainBinary(self,train1,train2,target_var):
		
		lgtrain = lgb.Dataset(
			train1[self.feature_list].values,
			train1[target_var].values,
			categorical_feature=self.str_feature_index_list
		)
		lgvalid = lgb.Dataset(
			train2[self.feature_list].values,
			train2[target_var].values,
			categorical_feature=self.str_feature_index_list
		)

		lgbm_params =  {
			'task': 'train',
			'boosting_type': 'gbdt',
			'objective': 'binary',
			'learning_rate': 0.1,
		}

		lgb_clf = lgb.train(
			lgbm_params,
			lgtrain,
			categorical_feature=self.str_feature_index_list,
			num_boost_round=1000,
			valid_sets=[lgtrain,lgvalid],
			valid_names=['train','valid'],
			early_stopping_rounds=100,
			verbose_eval=1
		)
		
		self.lgb_clf_list.append(lgb_clf)


	def validBinary(self):

		self.valid_data["score_lgb"] = 0.0
		
		cnt = 0
		f_cnt = 0
		for t_cnt in self.valid_query:

			cnt = cnt + 1
			print(str(cnt) + "/" + str(len(self.valid_query)))
			raceData = self.valid_data[f_cnt:t_cnt+f_cnt]

			for clf in self.lgb_clf_list:
				y_predict = clf.predict(raceData[self.feature_list].values)
				raceData["score_lgb"] = raceData["score_lgb"] + y_predict

			raceData["rank"] = raceData["score_lgb"].rank(method="first",ascending=False)

			for i in range(0,t_cnt):
				r_index = raceData.index[i]
				self.valid_data.at[f_cnt+i,"score_lgb"] = raceData.at[r_index,"score_lgb"]
				self.valid_data.at[f_cnt+i,"rank"] = raceData.at[r_index,"rank"]
			f_cnt = f_cnt + t_cnt

	def predictBinary(self,valid,lgb_clf_list):

		valid["score_lgb"] = 0.0

		for clf in lgb_clf_list:
			y_predict = clf.predict(valid[self.feature_list].values)
			valid["score_lgb"] = valid["score_lgb"] + y_predict

		valid["rank"] = valid["score_lgb"].rank(method="first",ascending=False)

		return valid.sort_values("rank")


	def predict(self):

		self.makeNormalizer()
		self.makeFeatureList()
		self.normalize()

		for i in range(0,len(self.train_data_list)):
			self.train_data_list[i]["勝"] = self.train_data_list[i]["人気"] / 3 > self.train_data_list[i]["着順"]

		for i in range(0,len(self.train_data_list)-1):
			self.trainBinary(
				self.train_data_list[i],
				self.train_data_list[i+1],
				"勝"
			)
		self.validBinary()
		self.valid_data[["日付","開催","R","score_lgb","着順","rank","単勝","馬場","天気","人気","コースの種類","レース条件"]].to_csv("result/predict.csv",index=False)

		importance = pd.DataFrame() 
		importance = pd.concat([pd.DataFrame(self.lgb_clf_list[0].feature_importance(),index=self.feature_list),importance],axis=1)
		importance.to_csv("result/importance.csv",sep="\t")
