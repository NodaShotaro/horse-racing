
import pandas as pd
import lightgbm as lgb
import math
import os
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from . import normalizeDF
from . import targetVar

class PredictionModel():

	def __init__(self):
		self.normalizer = normalizeDF.normalizeDF()
		self.num_features= []
		self.str_features= []
		self.lgb_clf_list  = []
		self.lgb_clf_ninki_list  = []
		self.feature_list  = []
		self.str_feature_index_list = []		
		self.lgbm_params =  {
			'task': 'train',
			'boosting_type': 'gbdt',
			'objective': 'binary',
			'learning_rate': 0.1,
		}
		self.target_data = pd.DataFrame()
		self.valid_data = pd.DataFrame()

	def loadTrainData(self,train_data_paths):
		self.train_data_list = []
		for path in train_data_paths:
			self.train_data_list.append(pd.read_csv(path))

	def loadTargetData(self,target_data_path):
		self.target_data = pd.read_csv(target_data_path)
		self.target_data["年齢"] = self.target_data["年齢"].astype("int")

	def loadValidData(self,valid_data_path,valid_query_path):
		self.valid_data = pd.read_csv(valid_data_path)
		self.valid_query = pd.read_csv(valid_query_path)["レース"]

	def setResultPath(self,result_path):
		self.result_path = result_path

	def setNumFeatures(self,num_features):
		self.num_features= num_features

	def setStrFeatures(self,str_features):
		self.str_features= str_features

	def setParam(lgbm_params):
		self.lgbm_params = lgbm_params

	def makeNormalizer(self):
		df = pd.DataFrame()
		df = pd.concat([df,self.valid_data,self.target_data])
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

		if len(self.valid_data) != 0:
			self.valid_data = self.normalizeCategories(self.valid_data)
			self.valid_data = self.normalizeNum(self.valid_data)

		if len(self.target_data) != 0:
			self.target_data = self.normalizeCategories(self.target_data)
			self.target_data = self.normalizeNum(self.target_data)
	
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

		lgb_clf = lgb.train(
			self.lgbm_params,
			lgtrain,
			categorical_feature=self.str_feature_index_list,
			num_boost_round=1000,
			valid_sets=[lgtrain,lgvalid],
			valid_names=['train','valid'],
			early_stopping_rounds=2,
			verbose_eval=1
		)
		
		self.lgb_clf_list.append(lgb_clf)



	def predictBinary(self):

		self.valid_data[self.target_var+"_p"] = 0.0
		
		cnt = 0
		f_cnt = 0
		for t_cnt in self.valid_query:
			cnt = cnt + 1
			print(str(cnt) + "/" + str(len(self.valid_query)))
			raceData = self.valid_data[f_cnt:t_cnt+f_cnt]
			raceData = self.predictBinaryRace(raceData)

			for i in range(0,t_cnt):
				r_index = raceData.index[i]
				self.valid_data.at[f_cnt+i,self.target_var+"_p"] = raceData.at[r_index,self.target_var+"_p"]
				self.valid_data.at[f_cnt+i,self.target_var+"_p_mean"] = raceData.at[r_index,self.target_var+"_p_mean"]
				self.valid_data.at[f_cnt+i,"rank"] = raceData.at[r_index,"rank"]
			f_cnt = f_cnt + t_cnt

	def predictBinaryRace(self,raceData):

		raceData[self.target_var+"_p"] = 0.0
		for clf in self.lgb_clf_list:
			y_predict = clf.predict(raceData[self.feature_list].values)
			raceData[self.target_var+"_p"] = raceData[self.target_var+"_p"] + y_predict / len(self.lgb_clf_list)

		raceData[self.target_var+"_p"] = raceData[self.target_var+"_p"] / len(self.lgb_clf_list)
		raceData[self.target_var+"_p_mean"] = raceData[self.target_var+"_p"] / raceData[self.target_var+"_p"].mean()
		raceData["rank"] = raceData[self.target_var+"_p"].rank(method="first",ascending=False)
		
		return raceData

	def predictTarget(self):
		output_features = [
			"日付",
			"開催",
			"レース条件",
			"馬番",
			"馬名",
			"rank",
			"R",
			self.target_var+"_p",
			self.target_var+"_p_mean",
		]
		df = self.predictBinaryRace(self.target_data).sort_values("rank")
		df[output_features].to_csv(self.result_path,index=False)

	def train(self,target_var):

		self.lgb_clf_list = []
		self.makeNormalizer()
		self.makeFeatureList()
		self.normalize()
		self.target_var = target_var

		self.lgbm_params =  {
			'task': 'train',
			'boosting_type': 'gbdt',
			'objective': 'regression',
			'learning_rate': 0.1,
		}

		for i in range(0,len(self.train_data_list)):
			self.train_data_list[i] = targetVar.calc(self.train_data_list[i])
			self.train_data_list[i]["30倍以下"] = self.train_data_list[i]["単勝"] <= 30
			self.train_data_list[i]["1着率"] = self.train_data_list[i]["着差"] <= 0.1

		for i in range(0,len(self.train_data_list)-1):
			self.trainBinary(
				self.train_data_list[i],
				self.train_data_list[i+1],
				target_var
			)

	def predict(self):
		self.predictBinary()

	def writeData(self):
		(self.valid_data).to_csv("result/predict.csv",index=False)

		importance = pd.DataFrame() 
		importance = pd.concat([pd.DataFrame(self.lgb_clf_list[0].feature_importance(),index=self.feature_list),importance],axis=1)
		importance.to_csv("result/importance.csv",sep="\t")
