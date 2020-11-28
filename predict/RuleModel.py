from .oishisa import normal
from .oishisa import even

def calcRank(df,df_query,result_path):

    cnt = 0
    f_cnt = 0
    df = even.calc(df)

    df["score_lgb"] = df["勝"]
    df["rank"] = 20
    for t_cnt in df_query:
        cnt = cnt + 1
        raceData = df[f_cnt:t_cnt+f_cnt]
        raceData["rank"] = raceData["score_lgb"].rank(method="first",ascending=False)
        raceData["rank_dup"] = raceData["score_lgb"].rank(method="min",ascending=False)
    
        for i in range(0,t_cnt):
            r_index = raceData.index[i]
            df.at[f_cnt+i,"rank"] = raceData.at[r_index,"rank"]
            df.at[f_cnt+i,"rank_dup"] = raceData.at[r_index,"rank_dup"]
        f_cnt = f_cnt + t_cnt
    df = df.sort_values("rank")
    df.to_csv(result_path,index=False)
