
import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# データセットの整形・欠損対策
class normalizeDF:

	def __init__(self):
		self.dim_mean = {}
		self.dim_std = {}
		self.dim_encoder = {}

	def register(self,ds,dimName):

		self.dim_mean[dimName] = ds.mean()
		self.dim_std[dimName] = ds.std()

		return 

	def registEncoder(self,ds,dimName):

		tmp_ds = ds.fillna("NULL")
		tmp_ds = ds.astype("str")

		self.dim_encoder[dimName] = LabelEncoder()
		self.dim_encoder[dimName] = self.dim_encoder[dimName].fit(tmp_ds)

		return

	def normalize(self,ds,dimName):

		# ds = ds - self.dim_mean[dimName]
		# ds = ds / self.dim_std[dimName]

		return ds

	def transform(self,ds,dimName):

		print(dimName)
		tmp_ds = ds.fillna("NULL")
		tmp_ds = ds.astype("str")

		tmp_ds =  self.dim_encoder[dimName].transform(tmp_ds)
		try:
			nullLabel = self.dim_encoder[dimName].inverse_transform(["NULL"])
			return tmp_ds.replace(nullLabel[0],None)
		except:
			return tmp_ds
