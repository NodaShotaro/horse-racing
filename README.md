
TODO  : パスワードベタ書きとかいう終わりコンテンツ直す

## crowling

### parseNetkeiba

netkeibaに直接アクセスするモジュール。

- parseRaceURL(yRange)
  - netkeiba上では，中央競馬が開催された日には各場の各レースへアクセスするためのページが生成されている
    - yRange[0]以上，yRange[1]未満の年に開催された上記ページのURLをListに変換して返す
- parseBreederComment(session,url)
  - 厩舎コメントのurlへsessionを使ってアクセスし，中身をテキスト形式で返す
- parseTraining(session,url)
  - 調教タイムのページを持つurlへsessionを使ってアクセスし，中身をDataFrame型に変換して返す
- parseHorse(session,url)
  - 馬の詳細ページを持つurlへsessionを使ってアクセスし，中身をDataFrame型に変換して返す
- parseRaceResult(session,url)
  - レースの詳細ページを持つurlへsessionを使ってアクセスし，中身をDataFrame型に変換して返す

### crowl

netkeibaへアクセスするモジュールのラッパー

- crowlRace(session,race_url_list)
  - crowlRaceURLで抽出したurl_listに記録された各ページからレースデータをパースし，DataFrame型にして返す

- crowlHorse(session,horse_url_list)
  - horse_url_listに記録された馬の詳細ページリストからレースデータをパースし，DataFrame型にして返す

- crowlTraining(session,training_url_list)
  - training_url_listに記録された調教タイムの詳細ページリストからレースデータをパースし，DataFrame型にして返す


## cleaning

### clean

raceTable、horseTable、trainTableに共通するクリーニング処理部分をいれた

### encode

raceTable、horseTable、trainTableに共通するカテゴリのエンコード処理部分をいれた

### cleanWrapper

cleanのラッパーと共通しないclean部分がここに残されてしまっている。うまく分割できていない。

## featureEngineering

特徴変換。いまは過去5走のみ。