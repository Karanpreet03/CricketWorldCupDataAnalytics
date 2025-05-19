import pandas as pd
import json

with open('t20_json_files/t20_json_files/t20_wc_match_results.json') as f:
    data = json.load(f)
df_match = pd.DataFrame(data[0]['matchSummary'])
df_match.rename({'scorecard': 'match_id'}, axis=1, inplace=True)
match_id_dct = {}
for index, row in df_match.iterrows():
    key1 = row["team1"] + ' Vs ' + row['team2']
    key2 = row["team2"] + " Vs " + row['team1']
    match_id_dct[key1] = row["match_id"]
    match_id_dct[key2] = row["match_id"]
df_match.to_csv('t20_csv_files/t20_wc_match_summary.csv', index=False)
# Batting summary
with open('t20_json_files/t20_json_files/t20_wc_batting_summary.json')as b:
    data = json.load(b)
    allRecords = []
    for rec in data:
        allRecords.extend(rec['battingSummary'])
df_batting = pd.DataFrame(allRecords)
df_batting["out/not_out"] = df_batting.dismissal.apply(lambda x : "out" if len(x)>0 else "not out")
df_batting["match_id"] = df_batting["match"].map(match_id_dct)
df_batting["batsmanName"] = df_batting['batsmanName'].apply(lambda x: x.replace('â€', ''))
df_batting.drop(columns=["dismissal"], inplace = True)
df_batting.to_csv('t20_csv_files/t20_wc_batting_summary.csv', index=False)
# Bowling Summary
with open('t20_json_files/t20_json_files/t20_wc_bowling_summary.json')as c:
    data = json.load(c)
    allBowlingRecords = []
    for rec in data:
        allBowlingRecords.extend(rec['bowlingSummary'])
df_bowling = pd.DataFrame(allBowlingRecords)
df_bowling["match_id"] = df_bowling["match"].map(match_id_dct)
df_bowling.to_csv('t20_csv_files/t20_wc_bowling_summary.csv', index=False)
# Player profile
with open('t20_json_files/t20_json_files/t20_wc_player_info.json') as d:
    data = json.load(d)
df_player = pd.DataFrame(data)
df_player.drop(columns=["description"], inplace=True)
df_player.to_csv('t20_csv_files/t20_wc_player_info_without_picture.csv', index = False)
