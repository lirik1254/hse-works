import json
import pandas as pd
from utils.DataPrepareUtils import data_prepare



# Балансирует данные для обучения модели (кол-во отзывов каждой тональности в списках =
# самому наименьшему кол-ву отзывов из всех тональностей
def process_category(data, category, result_list, limit):
    for key, value in data.items():
        for text in value[category]:
            result_list.append(text)
            if len(result_list) == limit:
                return


# Создаём датафрейм со столбцом отзывов и столбцом тональности отзыва
def preprocess_data(positive_list, negative_list, neutral_list):
    reviews_list = list()
    labels_list = list()
    for i in range(len(positive_list)):
        reviews_list.append(data_prepare(positive_list[i]))
        labels_list.append("positives")
        reviews_list.append(data_prepare(negative_list[i]))
        labels_list.append("negatives")
        reviews_list.append(data_prepare(neutral_list[i]))
        labels_list.append("neutral")
    return pd.DataFrame({'text': reviews_list, 'label': labels_list})


# Позволяет предсказывать тональность отзыва по тексту
def predict_sentiment(new_text, model, vectorizer, label_encoder):
    new_text_tfidf = vectorizer.transform([data_prepare(new_text)])
    predicted_label_encoded = model.predict(new_text_tfidf)[0]
    predicted_label = label_encoder.inverse_transform([predicted_label_encoded])[0]

    return predicted_label