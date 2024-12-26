from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import numpy as np

nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('russian'))
lemmatizer = WordNetLemmatizer()

# Загрузка модели
model = load_model('sentiment_analysis.keras')

# Токенизатор и лейбл-энкодер
tokenizer = Tokenizer(num_words=5000)  # Используем тот же токенизатор
label_encoder = LabelEncoder()

def clean_text(text):
    text = text.lower()  # Приведение текста к нижнему регистру
    text = re.sub(r'\d+', '', text)  # Удаляем цифры
    text = re.sub(r'[^\w\s]', '', text)  # Удаляем пунктуацию
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])  # Лемматизация и удаление стоп-слов
    return text


# Предсказание тональности сообщений
def predict_sentiment(messages):
    # Очистка текста и токенизация
    cleaned_messages = [clean_text(msg['text']) for msg in messages]
    tokenizer.fit_on_texts(cleaned_messages)
    sequences = tokenizer.texts_to_sequences(cleaned_messages)
    X = pad_sequences(sequences, padding='post', maxlen=100)

    # Получаем предсказания от модели
    y_pred = model.predict(X)
    predicted_classes = np.argmax(y_pred, axis=1)  # Получаем метки классов

    # Подсчитываем количество каждого класса
    sentiment_counts = {0: 0, 1: 0, 2: 0}  # 0 - нейтральный, 1 - положительный, 2 - негативный
    for sentiment in predicted_classes:
        sentiment_counts[sentiment] += 1

    return sentiment_counts

def plot_sentiment_pie_chart(sentiment_counts):
    labels = ['Нейтральные', 'Положительные', 'Негативные']
    sizes = [sentiment_counts[0], sentiment_counts[1], sentiment_counts[2]]

    # Построение pie chart
    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightgray', 'lightgreen', 'orangered'])
    plt.title("Распределение тональностей сообщений за сутки")

    # Сохранение графика в файл PNG
    plt.savefig('sentiment_pie_chart.png')
    plt.close()