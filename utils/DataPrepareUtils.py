import json
import string
import nltk
from nltk.corpus import stopwords

# Подготовка данных для обучения модели
def data_prepare(text):
    tokens = nltk.word_tokenize(text)  # Токенизируем
    tokens = [i for i in tokens if i not in string.punctuation and i != "—" and i != "»"  # Избавляемся от пунктуации
              and i != "..." and i != ".." and i != "«" and i[-1] != "." and i != "–" and i != "©" and
              i != "•"]
    tokens = [i.lower() for i in tokens]  # Приводим к нижнему регистру
    tokens = [i for i in tokens if i not in stopwords.words('russian')]  # Избавляемся от стоп-слов
    return " ".join(tokens)

# Загружает данные с json файла в словарь
def load_reviews_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data