import json
from datetime import datetime, timedelta

import pandas as pd
import requests
from joblib import load

from parseAPI import time_mas, home_mas, away_mas
from parseCountryLeague import country_mas, league_mas, league_id_mas, country_league_dict, \
    name_country_to_league_name_to_id_league_dict
import tkinter as tk
from tkinter import *
from tkinter import ttk
from io import BytesIO
from PIL import Image, ImageTk
import tkinter.font as tkfont

from googletrans import Translator

api_key = "2dafce4a5154755d6b75514c1e24b58b"

def update_options_for_country(event):
    selected_item_country = country_combo.get()
    try:
        values = list()
        for key in name_country_to_league_name_to_id_league_dict[selected_item_country]:
            values.append(key)
        league_by_country_combo.set(values[0])
        league_by_country_combo['values'] = values

        selected_item_league = league_by_country_combo.get()
        values = future_matches_by_league[
            str(name_country_to_league_name_to_id_league_dict[selected_item_country][selected_item_league])]
        future_matches_mas = list()
        for fixture in values['response']:
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            fixture_date = fixture['fixture']['date']
            # Переводим дату и время в формат Пермского времени (GMT+5)
            fixture_datetime = datetime.fromisoformat(fixture_date) + timedelta(hours=2)
            perth_time = fixture_datetime.strftime('%d.%m.%Y %H:%M')  # Форматируем в нужный формат
            string_to_append = f"{home_team} VS {away_team} {perth_time}"
            future_matches_mas.append(string_to_append)
        if len(future_matches_mas) == 0:
            future_matches_by_league_combo.set("Нет ближайший матчей")
            future_matches_by_league_combo['state'] = 'disabled'
        else:
            future_matches_by_league_combo['state'] = 'normal'
            future_matches_by_league_combo.set(future_matches_mas[0])
            future_matches_by_league_combo['values'] = future_matches_mas

    except KeyError:
        league_by_country_combo.set("Нет футбольных лиг в этой стране")


def update_options_for_league(event):
    selected_item_country = country_combo.get()
    selected_item_league = league_by_country_combo.get()
    values = future_matches_by_league[
        str(name_country_to_league_name_to_id_league_dict[selected_item_country][selected_item_league])]
    future_matches_mas = list()
    for fixture in values['response']:
        home_team = fixture['teams']['home']['name']
        away_team = fixture['teams']['away']['name']
        fixture_date = fixture['fixture']['date']
        # Переводим дату и время в формат Пермского времени (GMT+5)
        fixture_datetime = datetime.fromisoformat(fixture_date) + timedelta(hours=2)
        perth_time = fixture_datetime.strftime('%d.%m.%Y %H:%M')  # Форматируем в нужный формат
        string_to_append = f"{home_team} VS {away_team} {perth_time}"
        future_matches_mas.append(string_to_append)
    if len(future_matches_mas) == 0:
        future_matches_by_league_combo.set("Нет ближайший матчей")
        future_matches_by_league_combo.config(state="disabled")
    else:
        future_matches_by_league_combo['state'] = 'normal'
        future_matches_by_league_combo.set(future_matches_mas[0])
        future_matches_by_league_combo['values'] = future_matches_mas


def getImage(url):
    response = requests.get(url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    image = image.resize((100, 100))
    photo = ImageTk.PhotoImage(image)
    return photo


def get_id_league_by_name(league):
    for value in name_country_to_league_name_to_id_league_dict.values():
        if league in value.keys():
            return value[league]


def get_team_id(league_id, name):
    for fixture in future_matches_by_league[str(league_id)]['response']:
        if fixture['teams']['home']['name'] == name:
            return fixture['teams']['home']['id']
        elif fixture['teams']['away']['name'] == name:
            return fixture['teams']['away']['id']


def get_full_statistic_by_team(league_id, name_id):
    endpoint = 'https://v3.football.api-sports.io/teams/statistics'
    headers = {
        'x-rapidapi-host': 'v3.football.api-sports.io',
        'x-rapidapi-key': api_key
    }

    params = {
        'league': league_id,
        'team': name_id,
        'season': '2024'
    }

    response = requests.get(endpoint, headers=headers, params=params)
    response = response.json()
    home_mas = list()
    away_mas = list()
    all_mas = list()

    home_mas.append(response['response']['fixtures']['played']['home'])  # Общее кол-во сыгранных игр
    away_mas.append(response['response']['fixtures']['played']['away'])
    all_mas.append(response['response']['fixtures']['played']['total'])

    home_mas.append(response['response']['fixtures']['wins']['home'])  # Количество побед
    away_mas.append(response['response']['fixtures']['wins']['away'])
    all_mas.append(response['response']['fixtures']['wins']['total'])

    home_mas.append(response['response']['fixtures']['draws']['home'])  # Количество ничьих
    away_mas.append(response['response']['fixtures']['draws']['away'])
    all_mas.append(response['response']['fixtures']['draws']['total'])

    home_mas.append(response['response']['fixtures']['loses']['home'])  # Количество поражений
    away_mas.append(response['response']['fixtures']['loses']['away'])
    all_mas.append(response['response']['fixtures']['loses']['total'])

    home_mas.append(response['response']['goals']['for']['total']['home'])  # Количество забитых голов
    away_mas.append(response['response']['goals']['for']['total']['away'])
    all_mas.append(response['response']['goals']['for']['total']['total'])

    home_mas.append(response['response']['goals']['against']['total']['home'])  # Количество пропущенных голов
    away_mas.append(response['response']['goals']['against']['total']['away'])
    all_mas.append(response['response']['goals']['against']['total']['total'])

    home_mas.append(response['response']['goals']['for']['average']['home'])  # Среднее кол-во забитых голов
    away_mas.append(response['response']['goals']['for']['average']['away'])
    all_mas.append(response['response']['goals']['for']['average']['total'])

    home_mas.append(response['response']['goals']['against']['average']['home'])  # Среднее кол-во пропущенных голов
    away_mas.append(response['response']['goals']['against']['average']['away'])
    all_mas.append(response['response']['goals']['against']['average']['total'])

    home_away_all_mas = list()  # Массив ответов 0 индекс - дом, 1 индекс - чужое поле, 2 индекс - общее
    home_away_all_mas.append(home_mas)
    home_away_all_mas.append(away_mas)
    home_away_all_mas.append(all_mas)

    return home_away_all_mas


def show_tree(window, full_stat_mas, team_name, is_first, first_column_width):
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview.Heading", font=('Helvetica', 25, 'bold'), background="#D2FFF8")
    style.configure("Treeview", font=('Helvetica', 15), rowheight=40)

    tree = ttk.Treeview(window, columns=('empty', 'Дома', 'Гости', 'Всего'), show='headings')

    tree.heading('empty', text=team_name, anchor=tk.W)
    tree.heading('Дома', text='Дома', anchor=tk.CENTER)
    tree.heading('Гости', text='Гости', anchor=tk.CENTER)
    tree.heading('Всего', text='Всего', anchor=tk.CENTER)

    tree.column('empty', width=first_column_width + 50, anchor=tk.W)
    tree.column('Дома', width=150, anchor=tk.CENTER)
    tree.column('Гости', width=150, anchor=tk.CENTER)
    tree.column('Всего', width=150, anchor=tk.CENTER)

    # добавляем данные
    words_list = ['Всего сыграно', 'Победы', 'Ничьи', 'Поражения', 'Забитые голы', 'Пропущенные голы',
                  'В среднем забито за матч', 'В среднем пропущено за матч']
    for i in range(len(full_stat_mas[0])):
        mas_to_append = list()
        if i == 4 or i == 6:
            if i == 4:
                mas_to_append.append("Голы")
            else:
                mas_to_append.append("Средние голы")
            mas_to_append.append("")
            mas_to_append.append("")
            mas_to_append.append("")
            tree.insert("", END, values=tuple(mas_to_append), tags=('turquoise_line',))
        mas_to_append = list()
        mas_to_append.append(words_list[i])
        for g in range(len(full_stat_mas)):
            mas_to_append.append(full_stat_mas[g][i])
        tree.insert("", END, values=tuple(mas_to_append))

    tree.tag_configure('turquoise_line', background="#D2FFF8", font=('Helvetica', 25, 'bold'))

    global tree_width
    tree_width = tree.winfo_width()

    if is_first:
        tree.place(x=(1920 - 2 * tree_width) / 3, y=500)
    else:
        tree.place(x=2 * (1920 - 2 * tree_width) / 3 + tree_width, y=500)

    new_window.update_idletasks()
    tree_width = tree.winfo_width()

    if is_first:
        tree.place(x=(1920 - 2 * tree_width) / 3, y=500)
    else:
        tree.place(x=2 * (1920 - 2 * tree_width) / 3 + tree_width, y=500)


def get_stadium_name(league_id, home, away):
    for fixture in future_matches_by_league[str(league_id)]['response']:
        if (fixture['teams']['home']['name'] == home or fixture['teams']['away']['name'] == home) and (
                fixture['teams']['home']['name'] == away or fixture['teams']['away']['name'] == away):
            if fixture['league']['country'] == 'Russia' or fixture['league']['country'] == 'Uzbekistan':
                return fixture['fixture']['venue']['name'] # Тут типа перевод должен быть стадиона
            else:
                return fixture['fixture']['venue']['name']

model_to_predict_home_score = load('model_to_predict_home_score')
model_to_predict_away_score = load('model_to_predict_away_score')
def open_future_match(num):
    win.withdraw()
    global new_window
    new_window = Toplevel(win)
    new_window.title(TITLE)
    new_window.state('zoomed')
    new_window.iconphoto(False, photo)
    new_window.wm_geometry(f"{XNOTINZOOM}x{YNOTINZOOM}+%d+%d" % (x, y))
    if num == 4:
        future_match = future_matches_by_league_combo.get()
        league_id = get_id_league_by_name(league_by_country_combo.get())
    elif num == 0:
        home = home_mas[matchIndex]
        away = away_mas[matchIndex]
        time = time_mas[matchIndex]
        future_match = home + " VS " + away + " " + time
        league_id = '238'
    elif num == 1:
        home = home_mas[matchIndex - 1]
        away = away_mas[matchIndex - 1]
        time = time_mas[matchIndex - 1]
        future_match = home + " VS " + away + " " + time
        league_id = '238'
    elif num == 2:
        home = home_mas[matchIndex - 2]
        away = away_mas[matchIndex - 2]
        time = time_mas[matchIndex - 2]
        future_match = home + " VS " + away + " " + time
        league_id = '238'
    elif num == 3:
        home = home_mas[matchIndex - 3]
        away = away_mas[matchIndex - 3]
        time = time_mas[matchIndex - 3]
        future_match = home + " VS " + away + " " + time
        league_id = '238'
    for i in range(len(home_team_mas)):  # Исправить баг с URAL VS URAL - удалять подстроку из строки
        if home_team_mas[i] in future_match:
            if home_team_mas[i] in future_match and (
                    future_match.index(home_team_mas[i]) + len(home_team_mas[i]) - 1 == len(future_match) - 1 or
                    future_match[future_match.index(home_team_mas[i]) + len(home_team_mas[i]) + 1] == "V"):
                home = home_team_mas[i]
                index_home = future_match.index(home)
                break
    for i in range(len(away_team_mas)):
        if away_team_mas[i] in future_match:
            if away_team_mas[i] in future_match and away_team_mas[i] != home and (
                    future_match.index(away_team_mas[i]) + len(away_team_mas[i]) + 16 == len(future_match) - 1 or
                    future_match[future_match.index(away_team_mas[i]) + len(away_team_mas[i]) + 1] == "V"):
                away = away_team_mas[i]
                index_away = future_match.index(away)
                break
    for i in range(len(fixture_date_mas)):
        if fixture_date_mas[i] in future_match:
            time = fixture_date_mas[i]
            break
    font = ("Arial", 25, "bold")
    if len(time) > len(home) + len(away) + 4:
        text = time
    else:
        text = home + " VS " + away
    font_obj = tkfont.Font(font=font)
    text_width = font_obj.measure(text)

    home_width = font_obj.measure(home)
    away_width = font_obj.measure(away)

    if index_away > index_home:
        left_team = tk.Label(new_window, text=f'{time}\n{home} VS {away}',  # Создание лейбла
                             font=('Arial', 25, 'bold'),
                             pady=40)
        left_team.place(x=960 - text_width // 2, y=85)

    else:
        right_team = tk.Label(new_window, text=f'{time}\n{away} VS {home}',  # Создание лейбла
                              font=('Arial', 25, 'bold'),
                              pady=40)
        right_team.place(x=new_window.winfo_screenwidth() // 2 - text_width // 2, y=85)

    home_photo = getImage(comand_name_url_dict[home])
    away_photo = getImage(comand_name_url_dict[away])

    home_label = tk.Label(new_window, image=home_photo)
    home_label.image = home_photo
    away_label = tk.Label(new_window, image=away_photo)
    away_label.image = away_photo

    home_label.place(x=new_window.winfo_screenwidth() // 2 - text_width // 2 - 150, y=135)
    away_label.place(x=new_window.winfo_screenwidth() // 2 + text_width // 2 + 45, y=135)

    home_team_id = get_team_id(league_id, home)
    home_statistic_mas = get_full_statistic_by_team(league_id, home_team_id)

    away_team_id = get_team_id(league_id, away)
    away_statistic_mas = get_full_statistic_by_team(league_id, away_team_id)

    first_font = font = ('Arial', 25, 'bold')
    second_font = font = ('Arial', 15)

    font_obj_first = tkfont.Font(font=first_font)
    font_obj_second = tkfont.Font(font=second_font)

    text_width_first = font_obj_first.measure(home)
    text_width_second = font_obj_first.measure(away)
    text_width_third = font_obj_second.measure("В среднем пропущено за матч")

    show_tree(new_window, home_statistic_mas, home, True, max(text_width_first, text_width_second, text_width_third))
    show_tree(new_window, away_statistic_mas, away, False, max(text_width_first, text_width_second, text_width_third))

    stadium_name = get_stadium_name(league_id, home, away)
    if stadium_name == None:
        stadium_name = "Неизвестно"
    else:
        tk.Label(new_window, text="Стадион: " + stadium_name, font=('Arial', 25, 'bold')).place(
            relx = 0.5, rely = 0.35, anchor = "center")

    tk.Label(new_window, text="Статистика по командам за сезон 2024", font=('Arial', 25, 'bold')).place(
        relx=0.5, rely=0.43, anchor="center")

    tk.Label(new_window, text="Прогноз", font=('Arial', 30, 'bold'), foreground="#17B317").place(
        relx=0.5, rely=0.05, anchor="center")

    with open("names_elo_dict", "r") as file:
        names_elo_dict = json.load(file)

    if home in names_elo_dict.keys() and away in names_elo_dict.keys():
        elo_values = pd.DataFrame({'home_elo': [names_elo_dict[home]],
                          'away_elo': [names_elo_dict[away]]})
        home_score = round(model_to_predict_home_score.predict(elo_values)[0])
        away_score = round(model_to_predict_away_score.predict(elo_values)[0])
    else:
        home_score = 1
        away_score = 1

    tk.Label(new_window, text=home_score, font=('Arial', 30, 'bold'), foreground="#17B317").place(
        x = 960 - text_width // 2 + home_width / 2, y = 215)

    tk.Label(new_window, text=away_score, font=('Arial', 30, 'bold'), foreground="#17B317").place(
        x=960 + text_width // 2 - away_width / 2, y=215)

    new_window.protocol("WM_DELETE_WINDOW", lambda: on_destroy_future_match())


def on_destroy_future_match():
    global new_window
    new_window.destroy()
    win.deiconify()
    win.state('zoomed')


TITLE = "Прогнозирование результатов спортивных состязаний"
IMAGE = "ball.png"
XNOTINZOOM = 1200  # Если сворачивает, то в таком разрешение
YNOTINZOOM = 675
HOWMUCHBUTTONSONSCREEN = 4
NUMBERINSTRING = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eight']

func_dict = {
    'first': lambda: open_future_match(0),
    'second': lambda: open_future_match(1),
    'third': lambda: open_future_match(2),
    'fourth': lambda: open_future_match(3)
}

win = tk.Tk()
win.title(TITLE)

photo = tk.PhotoImage(file=IMAGE)
win.iconphoto(False, photo)

win.state('zoomed')  # Изначально в расширенном окне открывается

x = (win.winfo_screenwidth() - XNOTINZOOM) / 2
y = (win.winfo_screenheight() - YNOTINZOOM) / 2

win.wm_geometry(f"{XNOTINZOOM}x{YNOTINZOOM}+%d+%d" % (x, y))  # И при сворачивании окно располагается по центру

future_football_matches = tk.Label(win, text='Ближайшие футбольные матчи',  # Создание лейбла
                                   font=('Arial', 25, 'bold'),
                                   pady=40)
future_football_matches.pack()

matchIndex = len(home_mas) - 1

for i in range(4):
    future_match_button = tk.Button(win, text='',
                                    command=func_dict[NUMBERINSTRING[i]], width=50, height=10, bd=6).place(
        x=70 + i * 470, y=200)

    font_obj = tkfont.Font(font=('Arial', 15))
    time_width = font_obj.measure(time_mas[matchIndex-i])
    matches_width = font_obj.measure(f'{home_mas[matchIndex - i]} VS {away_mas[matchIndex - i]}')


    tk.Label(win, text=f'{time_mas[matchIndex - i]}', fg='green', font = ('Arial', 15)).place(x=175 + i * 470, y=245, in_=future_match_button)
    tk.Label(win, text = f'\n{home_mas[matchIndex - i]} VS {away_mas[matchIndex - i]}', font = ('Arial', 15)).place(x=70 + i * 470 + (358 - matches_width) / 2, y=280, in_=future_match_button)

with open("futureMatchesByLeague.json", "r") as file:
    future_matches_by_league = json.load(file)

comand_name_url_dict = dict()
for key, value in future_matches_by_league.items():
    for i in range(len(future_matches_by_league[key]['response'])):
        name_home = future_matches_by_league[key]['response'][i]['teams']['home']['name']
        logo_home = future_matches_by_league[key]['response'][i]['teams']['home']['logo']
        name_away = future_matches_by_league[key]['response'][i]['teams']['away']['name']
        logo_away = future_matches_by_league[key]['response'][i]['teams']['away']['logo']
        comand_name_url_dict[name_home] = logo_home
        comand_name_url_dict[name_away] = logo_away

# Можно покрасивее оформить расположение комбобоксов относительно друг друга с помощью combobox.winfo_x() winfo_y()
bigfont = tkfont.Font(family="Arial",size=14)
win.option_add("*TCombobox*Listbox*Font", bigfont)

country_combo = ttk.Combobox(win, width=20, state="readonly", font = ('Arial', 14))
country_combo['values'] = list(sorted((set(country_mas))))
country_combo.place(x=75, y=510)
country_combo.set(country_mas[country_mas.index("Russia")])
country_combo.bind('<<ComboboxSelected>>', update_options_for_country)

league_by_country_combo = ttk.Combobox(win, values=list(set(league_mas)), width=35, state="readonly", font = ('Arial', 14))
league_by_country_combo.place(x=320, y=510)

try:
    what_set = list()
    keys_russia_append = list()
    for key in name_country_to_league_name_to_id_league_dict['Russia'].keys():
        keys_russia_append.append(key)
    league_by_country_combo.set(keys_russia_append[0])
    league_by_country_combo['values'] = keys_russia_append
except KeyError:
    league_by_country_combo.set("Нет футбольных лиг в этой стране")

league_by_country_combo.bind("<<ComboboxSelected>>", update_options_for_league)

future_matches_by_league_combo = ttk.Combobox(win, values=[], width=70, state="readonly", font = ('Arial', 14))
future_matches_by_league_combo.place(x=730, y=510)
selected_item_country = country_combo.get()
try:
    selected_item_league = league_by_country_combo.get()
    values = future_matches_by_league[
        str(name_country_to_league_name_to_id_league_dict[selected_item_country][selected_item_league])]
    future_matches_mas = list()
    for fixture in values['response']:
        home_team = fixture['teams']['home']['name']
        away_team = fixture['teams']['away']['name']
        fixture_date = fixture['fixture']['date']
        # Переводим дату и время в формат Пермского времени (GMT+5)
        fixture_datetime = datetime.fromisoformat(fixture_date) + timedelta(hours=2)
        perth_time = fixture_datetime.strftime('%d.%m.%Y %H:%M')  # Форматируем в нужный формат
        string_to_append = f"{home_team} VS {away_team} {perth_time}"
        future_matches_mas.append(string_to_append)
    if len(future_matches_mas) == 0:
        future_matches_by_league_combo.set("Нет ближайший матчей")
        future_matches_by_league_combo["state"] = "disabled"
    else:
        future_matches_by_league_combo.set(future_matches_mas[0])
        future_matches_by_league_combo['values'] = future_matches_mas

except KeyError:
    league_by_country_combo.set("Нет футбольных лиг в этой стране")

home_team_mas = list()
away_team_mas = list()
fixture_date_mas = list()

with open("futureMatchesByLeague.json", "r") as file:
    future_matches_by_league = json.load(file)

for i in range(len(league_id_mas)):
    values = future_matches_by_league[str(league_id_mas[i])]
    for fixture in values['response']:
        home_team = fixture['teams']['home']['name']
        home_team_mas.append(home_team)

        away_team = fixture['teams']['away']['name']
        away_team_mas.append(away_team)

        fixture_date = fixture['fixture']['date']

        # Переводим дату и время в формат Пермского времени (GMT+5)
        fixture_datetime = datetime.fromisoformat(fixture_date) + timedelta(hours=2)
        perth_time = fixture_datetime.strftime('%d.%m.%Y %H:%M')  # Форматируем в нужный формат

        fixture_date_mas.append(perth_time)

tk.Label(win, text='Выберите страну',
         font=('Arial', 14), bg="#accaf2").place(x=75, y=470)

tk.Label(win, text='Выберите лигу',
         font=('Arial', 14), bg="#accaf2").place(x=320, y=470)

tk.Label(win, text='Выберите матч',
         font=('Arial', 14), bg="#accaf2").place(x=730, y=470)

tk.Button(win, text='Перейти к матчу', width=25, height=3, bd=6, command=lambda: open_future_match(4), font = ('Arial', 14)).place(x=1550,
                                                                                                             y=508)

win.mainloop()
