
# 8.4% / 108.6 %
def calc(df):
    df["勝"] = df["人気"] / 3 >= df["着順"]
    return df

# 1.5% / 87.4 %
# def calc(df):
#     df["勝"] = df["人気"] - df["着順"]
#     return df

# 4.2% / 98.8 % 
# def calc(df):
#     df["勝"] = df["人気"] / df["着順"]
#     return df