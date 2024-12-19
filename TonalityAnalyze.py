from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from utils.TonalityAnalyzeUtils import process_category, preprocess_data, predict_sentiment
from utils.DataPrepareUtils import load_reviews_from_json

def load_and_process_reviews():
    data = load_reviews_from_json("reviews.json")
    positive_list = list()
    negative_list = list()
    neutral_list = list()
    LIMIT = 215

    # Собираем по 215 отзывов каждой тональности
    process_category(data, 'positives', positive_list, LIMIT)
    process_category(data, 'negatives', negative_list, LIMIT)
    process_category(data, 'neutral', neutral_list, LIMIT)

    return positive_list, negative_list, neutral_list

def train_model():
    positive_list, negative_list, neutral_list = load_and_process_reviews()
    # Создаём датафрейм со столбцом отзывов и столбцом тональности отзывов
    df = preprocess_data(positive_list, negative_list, neutral_list)
    print(df)

    label_encoder = LabelEncoder()
    df['label_encoded'] = label_encoder.fit_transform(df['label'])

    # Разделяем данные на обучающую и тестовую выборки
    X = df['text']
    y = df['label_encoded']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Обучение модели
    model = MultinomialNB()
    model.fit(X_train_tfidf, y_train)

    # Прогнозирование на тестовой выборке
    y_pred = model.predict(X_test_tfidf)
    return model, vectorizer, label_encoder, y_test, y_pred


def print_tonality_analyze():
    model, vectorizer, label_encoder, y_test, y_pred = train_model()

    text_bad = "Мне фильм не понравился какой-то он не крутой вообще фу 0 баллов"
    text_neutral = "Хотя сейчас я уже не испытываю от фильма тех же чувств, что и раньше, считаю огромной несправедливостью, что он не взял ни одного «Оскара». Очень жаль: у картины были все шансы."
    text_good = "Я в восторге от фильма, это просто невероятно, всем смотреть рекомендую!"

    print(text_bad + ": " + predict_sentiment(text_bad, model, vectorizer, label_encoder))
    print(text_neutral + ": " + predict_sentiment(text_neutral, model, vectorizer, label_encoder))
    print(text_good + ": " + predict_sentiment(text_good, model, vectorizer, label_encoder))
    print()

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Полный отчёт по классификации
    report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)
    print("Classification Report:")
    print(report)












