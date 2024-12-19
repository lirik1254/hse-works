from TonalityAnalyze import predict_sentiment
import matplotlib.pyplot as plt
from utils.DataPrepareUtils import load_reviews_from_json
from TonalityAnalyze import train_model


# Возвращает необходимые для построения графика данные
def process_reviews(data, predict_sentiment, model, vectorizer, label_encoder):
    good_prediction_count = 0
    bad_prediction_count = 0

    real_count_positives = 0
    real_count_negatives = 0
    real_count_neutral = 0

    model_count_positives = 0
    model_count_negatives = 0
    model_count_neutral = 0

    for key, value in data.items():
        for category in ['positives', 'negatives', 'neutral']:
            for text in value[category]:
                if category == 'positives':
                    real_count_positives += 1
                elif category == 'negatives':
                    real_count_negatives += 1
                elif category == 'neutral':
                    real_count_neutral += 1

                predicted_label = predict_sentiment(text, model, vectorizer, label_encoder)

                if predicted_label == 'positives':
                    model_count_positives += 1
                elif predicted_label == 'negatives':
                    model_count_negatives += 1
                elif predicted_label == 'neutral':
                    model_count_neutral += 1

                if predicted_label == category:
                    good_prediction_count += 1
                else:
                    bad_prediction_count += 1

    return {
        'good_predictions': good_prediction_count,
        'bad_predictions': bad_prediction_count,
        'real_counts': {
            'positives': real_count_positives,
            'negatives': real_count_negatives,
            'neutral': real_count_neutral
        },
        'model_counts': {
            'positives': model_count_positives,
            'negatives': model_count_negatives,
            'neutral': model_count_neutral
        }
    }


# Построение диаграммы, отражающей кол-во верно и неверно предсказанных категорий
def plot_pie_chart(result):
    labels = ['Good Predictions', 'Bad Predictions']
    sizes = [result['good_predictions'], result['bad_predictions']]
    colors = ['#4CAF50', '#F44336']
    explode = (0.1, 0)

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('Prediction Accuracy')
    plt.axis('equal')
    plt.show()

# Построение распределения кол-ва отзывов, относящихся к определенной категории
def plot_distribution_pie_chart(counts, title):
    labels = ['Positives', 'Negatives', 'Neutral']
    sizes = [counts['positives'], counts['negatives'], counts['neutral']]
    colors = ['#4CAF50', '#F44336', '#FFC107']

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title(title)
    plt.axis('equal')
    plt.show()

def build_charts():
    model, vectorizer, label_encoder, y_test, y_pred = train_model()
    data = load_reviews_from_json("reviews.json")
    result = process_reviews(data, predict_sentiment, model, vectorizer, label_encoder)

    successful_predictions = result['good_predictions']
    unsuccess_predictions = result['bad_predictions']
    all_data_accuracy = successful_predictions / (successful_predictions + unsuccess_predictions) * 100

    print(f"Точность на всех данных: {all_data_accuracy:.2f} %")

    # Строим графики, отображающие обученной модели
    plot_pie_chart(result)
    plot_distribution_pie_chart(result['real_counts'], 'Real Sentiment Distribution')
    plot_distribution_pie_chart(result['model_counts'], 'Model Predicted Sentiment Distribution')


