from parseCountryLeague import league_mas, league_id_mas, country_mas, country_league_dict
from datetime import datetime, timedelta
import time
import requests
import json

api_key = "243c2c09ee5de7da19612b20c8eb3e9d"
endpoint = 'https://v3.football.api-sports.io/fixtures'

headers = {
    'x-rapidapi-host': 'v3.football.api-sports.io',
    'x-rapidapi-key': api_key
}

params = {
    'league': '238',
    'timezone': 'Europe/Moscow',  # Установим часовой пояс Москвы (GMT+3)
    'next': '99'  # Количество ближайших матчей, которые вы хотите получить
}

future_matches_by_league = dict()


for i in range(len(league_id_mas)):
    params['league'] = league_id_mas[i]
    response = requests.get(endpoint, headers=headers, params=params)
    if response.status_code == 200:
        futureMatchesByLeague = response.json()
        future_matches_by_league[league_id_mas[i]] = futureMatchesByLeague
    print(f"{i + 1} ближайшие матчи по лиге получены")
    time.sleep(6)

with open("futureMatchesByLeague.json", "w") as file:
    json.dump(future_matches_by_league, file, indent=4)

# with open("futureMatchesByLeague.json", "r") as file:
#     future_matches_by_league = json.load(file)
