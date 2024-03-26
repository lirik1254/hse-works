import json
from datetime import datetime, timedelta

import requests

# api_key = "6f80acb74ba79f00ff39f60c1f252224"
# endpoint = 'https://v3.football.api-sports.io/leagues'
# #
# headers = {
#     'x-rapidapi-host': 'v3.football.api-sports.io',
#     'x-rapidapi-key': api_key
# }
#
# params = {
#     'season': '2024',
#     'current': 'true',
#     'last': '99'
# }
#
# response = requests.get(endpoint, headers=headers, params=params)
#
# if response.status_code == 200:
#     data = response.json()
#     with open('data.json', 'w') as file:
#         json.dump(data, file, indent=4)

with open("data.json", "r") as file:
    data = json.load(file)

league_mas = list()
country_mas = list()
league_id_mas = list()
country_league_dict = dict()

for fixture in data['response']:
    league = fixture['league']['name']
    country = fixture['country']['name']
    id = fixture['league']['id']
    league_mas.append(league)
    country_mas.append(country)
    league_id_mas.append(id)


name_country_to_league_name_to_id_league_dict = dict()

for fixture in data['response']:
    league = fixture['league']['name']
    country = fixture['country']['name']
    id = fixture['league']['id']
    try:
        name_country_to_league_name_to_id_league_dict[country][league] = id
    except KeyError:
        name_league_id_league_dict = dict()
        name_league_id_league_dict[league] = id
        name_country_to_league_name_to_id_league_dict[country] = name_league_id_league_dict










