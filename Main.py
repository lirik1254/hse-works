from TonalityAnalyze import print_tonality_analyze
from utils.ChartsUtils import build_charts
from KinopoiskScrap import parse

# Парсим данные с кинопоиска (займёт часа 2-3)
parse()

# Печатает информацию об обученной модели
print_tonality_analyze()

# Строит графики (займёт минут 5)
build_charts()
