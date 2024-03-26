import json
from datetime import datetime, timedelta
#
# import requests
#
# api_key = "6f80acb74ba79f00ff39f60c1f252224"
# endpoint = 'https://v3.football.api-sports.io/fixtures'
#
# headers = {
#     'x-rapidapi-host': 'v3.football.api-sports.io',
#     'x-rapidapi-key': api_key
# }
#
# params = {
#     'league': '238',
#     'timezone': 'Europe/Moscow',  # Установим часовой пояс Москвы (GMT+3)
#     'next': '4'  # Количество ближайших матчей, которые вы хотите получить
# }
#
# response = requests.get(endpoint, headers=headers, params=params)
# print(response.text)
#
# home_teams = list()
# away_teams = list()
# time = list()
#
# if response.status_code == 200:
#     futureMatches = response.json()
#     with open('futureMatches.json', 'w') as file:
#         json.dump(futureMatches, file, indent=4)

with open("futureMatches.json", "r") as file:
    futureMatches = json.load(file)

time_mas = list()
home_mas = list()
away_mas = list()

for fixture in futureMatches['response']:
    home_team = fixture['teams']['home']['name']
    away_team = fixture['teams']['away']['name']
    fixture_date = fixture['fixture']['date']
    # Переводим дату и время в формат Пермского времени (GMT+5)
    fixture_datetime = datetime.fromisoformat(fixture_date) + timedelta(hours=2)
    perth_time = fixture_datetime.strftime('%d.%m.%Y %H:%M')  # Форматируем в нужный формат
    time_mas.append(perth_time)
    home_mas.append(home_team)
    away_mas.append(away_team)

# endpoint = 'https://v3.football.api-sports.io/teams/statistics'
#
# headers = {
#     'x-rapidapi-host': 'v3.football.api-sports.io',
#     'x-rapidapi-key': api_key
# }
#
# params = {
#     'league': '238',
#     'team': '15176',
#     'season': '2024'
# }
#
# response = requests.get(endpoint, headers=headers, params=params)

# if response.status_code == 200:
#     team_statistic = response.json()
#     with open('team_statistic.json', 'w') as file:
#         json.dump(team_statistic, file, indent=4)

# with open("team_statistic.json", "r") as file:
#     team_statistic = json.load(file)
#
#
# # print(team_statistic)
# print("Games played " + str(team_statistic['response']['fixtures']['played']['home']) + " " + str(team_statistic['response']['fixtures']['played']['away']) + " " + str(team_statistic['response']['fixtures']['played']['total']))
# print("Draws")







