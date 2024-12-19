import json
from selenium import webdriver
from utils.ScrapUtils import parse_movie_text
from utils.ScrapUtils import get_link_list


def parse_link_list(driver):
    # Получаем 250 ссылок на 250 лучших фильмов
    link_list = list()
    for i in range(1, 6):
        temp_link_list = get_link_list(f"https://www.kinopoisk.ru/lists/movies/top250/?page={i}", driver)
        for g in temp_link_list:
            link_list.append(g)
    print(len(link_list))
    return link_list


def parse_reviews_list(driver):
    link_list = parse_link_list(driver)
    # Получаем позитивные, негативные, нейтральные отзывы по 3 фильмам
    all_reviews = {}
    i = 1
    for movie_url in link_list:
        print(i)
        movie_text = parse_movie_text(movie_url, driver)
        while movie_text == {}:
            movie_text = parse_movie_text(movie_url, driver)
        for key, value in movie_text.items():
            print(key)
            all_reviews[key] = value
        i += 1

    # Записываем в json файл
    with open("reviews.json", "w", encoding="utf-8") as f:
        json.dump(all_reviews, f, ensure_ascii=False, indent=4)


def parse():
    driver = webdriver.Chrome()
    parse_reviews_list(driver)
    driver.quit()


