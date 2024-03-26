import time
from datetime import datetime, timedelta

from joblib import load
from joblib import dump
import numpy as np
import openpyxl
import pandas as pd

import requests
import json
from parseCountryLeague import league_id_mas

# api_key = "36ea1281e34ac40edd2c81aa0cf9476d"
# endpoint = 'https://v3.football.api-sports.io/fixtures'
#
# headers = {
#     'x-rapidapi-host': 'v3.football.api-sports.io',
#     'x-rapidapi-key': api_key
# }
#
# params = {
#   # Установим часовой пояс Москвы (GMT+3)
#     'league': '71',
#     'from': '2018-01-01',
#     'to': '2018-12-31',
#     'season': 2018
# }
#
#
# last_matches_year_dict = dict()
#
season_list = [2022, 2023]
# for i in range(len(season_list)):
#     load_last_matches_dict = dict()
#     if i == 1:
#         api_key = "36ea1281e34ac40edd2c81aa0cf9476d"
#         headers['x-rapidapi-key'] = api_key
#     params['from'] = str(season_list[i]) + params['from'][4::]
#     params['to'] = str(season_list[i]) + params['to'][4::]
#     params['season'] = season_list[i]
#     for g in range(len(league_id_mas)):
#         params['league'] = str(league_id_mas[g])
#         response = requests.get(endpoint, headers = headers, params=params)
#         last_matches = response.json()
#         load_last_matches_dict[str(league_id_mas[g])] = last_matches
#         print(f" {g+1} запись по {season_list[i]} сезону получена")
#         time.sleep(6)
#     last_matches_year_dict[season_list[i]] = load_last_matches_dict
#     print("\n")
#
#
#
# with open('last_matches.json', 'w') as file:
#     json.dump(last_matches_year_dict, file, indent=4)

# last_matches_dict = dict()
# with open("last_matches.json", "r") as file:
#     last_matches_dict = json.load(file)
#
#
# last_matches_mas = list()
# for i in range(len(season_list)):
#     for g in range(len(league_id_mas)):
#         for fixture in last_matches_dict[str(season_list[i])][str(league_id_mas[g])]['response']:
#             match_dict = dict()
#             date = datetime.fromisoformat(fixture['fixture']['date']) + timedelta(hours=2)
#             date = date.strftime('%d.%m.%Y %H:%M')
#             home_name = fixture['teams']['home']['name']
#             away_name = fixture['teams']['away']['name']
#             home_id = fixture['teams']['home']['id']
#             away_id = fixture['teams']['away']['id']
#             fixture_id = fixture['fixture']['id']
#             home_score = fixture['goals']['home']
#             away_score = fixture['goals']['away']
#             match_dict['date'] = date
#             match_dict['home_name'] = home_name
#             match_dict['away_name'] = away_name
#             match_dict['home_id'] = home_id
#             match_dict['away_id'] = away_id
#             match_dict['fixture_id'] = fixture_id
#             match_dict['home_score'] = home_score
#             match_dict['away_score'] = away_score
#             last_matches_mas.append(match_dict)
#
# home_name_mas = list()
# away_name_mas = list()
# home_id_mas = list()
# away_id_mas = list()
# date_mas = list()
# home_score_mas = list()
# away_score_mas = list()
# fixture_id_mas = list()
#
# for i in range(len(last_matches_mas)):
#     home_name_mas.append(last_matches_mas[i]['home_name'])
#     away_name_mas.append(last_matches_mas[i]['away_name'])
#     home_id_mas.append(last_matches_mas[i]['home_id'])
#     away_id_mas.append(last_matches_mas[i]['away_id'])
#     date_mas.append(last_matches_mas[i]['date'])
#     home_score_mas.append(last_matches_mas[i]['home_score'])
#     away_score_mas.append(last_matches_mas[i]['away_score'])
#     fixture_id_mas.append(last_matches_mas[i]['fixture_id'])
#
# data = {
#     'date': date_mas,
#     'home_name': home_name_mas,
#     'away_name': away_name_mas,
#     'home_score': home_score_mas,
#     'away_score': away_score_mas,
#     'home_id': home_id_mas,
#     'away_id': away_id_mas,
#     'fixture_id': fixture_id_mas
# }

# df = pd.read_excel('2022_2023_matches.xlsx')

# names_set = set()
# for i in range(len(df['home_name'])):
#     names_set.add(df['home_name'][i])
# for i in range(len(df['away_name'])):
#     names_set.add(df['away_name'][i])
#
# print(len(names_set))
#
# with open('futureMatchesByLeague.json', 'r') as file:
#     future_matches_dict = json.load(file)
#
# names_set1 = set()
# for key in future_matches_dict.keys():
#     for fixture in future_matches_dict[key]['response']:
#         names_set1.add(fixture['teams']['home']['name'])
#         names_set1.add(fixture['teams']['away']['name'])

# print("Длина прошлых матчей: " + str(len(names_set)))
# print("Длина будущих матчей: " + str(len(names_set1)))
# print("Пересечение: " + str(len(names_set.intersection(names_set1))))

# names_elo_dict = dict()
# for name in names_set:
#     names_elo_dict[name] = 2400
#
# for i in range(len(df)):
#     home_name = df['home_name'][i]
#     away_name = df['away_name'][i]
#     home_score = df['home_score'][i]
#     away_score = df['away_score'][i]
#     if home_score > away_score:
#         names_elo_dict[home_name] += (10 + (home_score - away_score) * 2)
#         names_elo_dict[away_name] -= (10 + (home_score - away_score) * 2)
#     elif home_score == away_score and names_elo_dict[home_name] - names_elo_dict[away_name] > 50:
#         names_elo_dict[away_name] += 5
#     elif home_score == away_score and names_elo_dict[away_name] - names_elo_dict[home_name] > 50:
#         names_elo_dict[home_name] += 3
#     elif home_score < away_score:
#         names_elo_dict[home_name] -= (10 + (away_score - home_score) * 2)
#         names_elo_dict[away_name] += (10 + (away_score - home_score) * 2 )
#
# with open('names_elo_dict', 'w') as file:
#     json.dump(names_elo_dict, file, indent=4)
#
# df['home_elo'] = [2400 for i in range(len(df))]
# df['away_elo'] = [2400 for i in range(len(df))]
#
# pd.options.mode.chained_assignment = None
#
# for i in range(len(df)):
#     df['home_elo'][i] = names_elo_dict[df['home_name'][i]]
#     df['away_elo'][i] = names_elo_dict[df['away_name'][i]]
#
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import roc_auc_score
#
# df_to_predict_home_score = pd.DataFrame({'home_elo': df['home_elo'],
#                                          'away_elo': df['away_elo'],
#                                         'home_score': df['home_score']})
#
# df_to_predict_away_score = pd.DataFrame({'home_elo': df['home_elo'],
#                                          'away_elo': df['away_elo'],
#                                         'away_score': df['away_score']})
#
# X_train_home, X_test_home, y_train_home, y_test_home = train_test_split(
#     df_to_predict_home_score[['home_elo', 'away_elo']],
#     df_to_predict_home_score['home_score'], test_size=0.2, random_state = 42
# )
#
# X_train_away, X_test_away, y_train_away, y_test_away = train_test_split(
#     df_to_predict_away_score[['home_elo', 'away_elo']],
#     df_to_predict_away_score['away_score'], test_size=0.2, random_state = 42
# )
#
# y_train_home = y_train_home.fillna(1.0)
# y_test_home = y_test_home.fillna(1.0)
#
# y_test_away = y_test_away.fillna(1.0)
# y_train_away = y_train_away.fillna(1.0)
#
# print(X_test_home)
#
# model_to_predict_home_score = RandomForestRegressor(n_estimators=100,
#                                                     random_state=1,
#                                                     oob_score = True)
# model_to_predict_home_score.fit(X_train_home, y_train_home)
#
#
#
# model_to_predict_away_score = RandomForestRegressor(n_estimators=100,
#                                                     random_state=1,
#                                                     oob_score = True)
# model_to_predict_away_score.fit(X_train_away, y_train_away)

# dump(model_to_predict_home_score, 'model_to_predict_home_score')
# dump(model_to_predict_away_score, 'model_to_predict_away_score')

from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error



# print(mean_absolute_percentage_error(y_test_home, home_score_predicts_float))
# print(mean_squared_error(y_test_home, home_score_predicts_float))
