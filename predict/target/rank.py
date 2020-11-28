
#ﾀｲﾑ指数
def calc(df):
    df["勝"] = df["着差"] <= 0.1
    return df
