import string
import pymorphy2
import nltk
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem import SnowballStemmer

nltk.download('punkt')
nltk.download('stopwords')


# Метод для подготовки данных (выделение токенов, избавление от пунктуации, стоп слов
def data_prepare(text):
    tokens = nltk.word_tokenize(text)  # Токенизируем

    tokens = [i for i in tokens if i not in string.punctuation and i != "—" and i != "»"  # Избавляемся от пунктуации
              and i != "..." and i != ".." and i != "«" and i[-1] != "." and i != "–" and i != "©" and
              i != "•"]

    tokens = [i.lower() for i in tokens]  # Приводим к нижнему регистру

    tokens = [i for i in tokens if i not in stopwords.words('russian')]  # Избавляемся от стоп-слов
    tokens = [i for i in tokens if i != "че" and i != "ещё" and i != "ещё" and i != "это" and i != '"' and i != "чё"]
    return tokens


# Метод для построения частотного словаря через лемматизацию
def create_frequency_dict_lemma(text):
    tokens = data_prepare(text)
    pm = pymorphy2.MorphAnalyzer()
    tokens_lemma = [pm.parse(i.lower())[0].normal_form for i in tokens]  # Лемматизируем

    tokens_lemma = [i for i in tokens_lemma if i not in stopwords.words('russian')]  # Избавляемся от стоп-слов ещё раз,
    # поскольку лемматизация их порождает

    counter_lemma = Counter()  # Построение частотного словаря
    counter_lemma.update(tokens_lemma)

    counter_lemma = {key: value for key, value in counter_lemma.items() if not key.replace('.', '', 1).isdigit()}

    # Сортируем словарь по убыванию частоты
    return dict(sorted(counter_lemma.items(), key=lambda item: item[1], reverse=True))


# Метод для построения частотного словаря через стемминг
def create_frequency_dict_stemming(text):
    tokens = data_prepare(text)
    stemmer = SnowballStemmer('russian')

    tokens_stemma = [stemmer.stem(i) for i in tokens]  # Стеммируем

    tokens_stemma = [i for i in tokens_stemma if
                     i not in stopwords.words('russian')]  # Избавляемся от стоп-слов ещё раз,
    # поскольку стемминг их порождает

    counter_stemma = Counter()  # Построение частотного словаря
    counter_stemma.update(tokens_stemma)

    counter_stemma = dict(sorted(counter_stemma.items(), key=lambda item: item[1], reverse=True))

    return counter_stemma
