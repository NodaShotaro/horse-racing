
import pandas as pd
import numpy as np
from datetime import datetime as dt

from calcReturn import single

df = pd.read_csv("result/predict.csv")

single.calcSingle(df)
for i,t in df.groupby("レース条件"):
    print(i)
    single.calcSingle(t)