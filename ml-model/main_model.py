from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import scipy.sparse as sp
import joblib
import warnings
from transformers import pipeline
import pandas as pd

# Suppress warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Initialize sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def preprocess_text(text):
    return text.lower() if isinstance(text, str) else ""

def analyze_sentiment(article):
    if article:
        try:
            sentiment = sentiment_pipeline(article[:512])  # Limit text length
            return sentiment[0]['score'] if sentiment[0]['label'] == 'POSITIVE' else -sentiment[0]['score']
        except Exception:
            return 0
    return 0

def preprocess_data(df):
    df = df.dropna(subset=['article_text', 'title'])
    df['sentiment_score'] = df['article_text'].apply(analyze_sentiment)
    df['article_text'] = df['article_text'].apply(preprocess_text)
    df['title'] = df['title'].apply(preprocess_text)
    return df

def extract_features(df):
    vectorizer_article = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
    vectorizer_title = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))

    X_article = vectorizer_article.fit_transform(df['article_text'])
    X_title = vectorizer_title.fit_transform(df['title'])

    X = sp.hstack((X_article, X_title), format='csr')
    y = df['sentiment_score']

    return X, y, vectorizer_article, vectorizer_title

def train_sentiment_model():
    print("Loading dataset...")
    df = pd.read_csv("preprocessed_data.csv")
    print(f"Dataset loaded. Shape: {df.shape}")

    df = preprocess_data(df)
    X, y, vectorizer_article, vectorizer_title = extract_features(df)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"MSE: {mse}, R²: {r2}")

    # Save model and vectorizers
    joblib.dump(model, 'sentiment_model.pkl')
    joblib.dump(vectorizer_article, 'tfidf_vectorizer_article.pkl')
    joblib.dump(vectorizer_title, 'tfidf_vectorizer_title.pkl')

    return model, vectorizer_article, vectorizer_title, mse, r2

def predict_sentiment(new_article_text, new_title):
    print("Loading trained model and vectorizers...")
    model = joblib.load('sentiment_model.pkl')
    vectorizer_article = joblib.load('tfidf_vectorizer_article.pkl')
    vectorizer_title = joblib.load('tfidf_vectorizer_title.pkl')

    new_article_vectorized = vectorizer_article.transform([preprocess_text(new_article_text)])
    new_title_vectorized = vectorizer_title.transform([preprocess_text(new_title)])

    new_X = sp.hstack((new_article_vectorized, new_title_vectorized), format='csr')

    if new_X.shape[1] != model.coef_.shape[0]:
        print(f"Feature mismatch! Expected {model.coef_.shape[0]}, but got {new_X.shape[1]}")
        return None

    return model.predict(new_X)[0]

if __name__ == "__main__":
    print("Starting training process...")
    train_sentiment_model()
    print("Training complete.")

    test_cases = [
    # Positive cases
    {"article_text": "Bitcoin surged past $70,000 as institutional investors poured in.", "title": "Bitcoin breaks record high", "description": "Positive"},
    {"article_text": "Apple stock soared after reporting higher-than-expected earnings.", "title": "Apple beats earnings expectations", "description": "Positive"},
    {"article_text": "Ethereum's major upgrade improved transaction speeds and lowered fees.", "title": "Ethereum upgrade boosts performance", "description": "Positive"},
    {"article_text": "Tesla shares jumped 10% after strong vehicle delivery numbers.", "title": "Tesla stock soars on strong sales", "description": "Positive"},
    {"article_text": "The S&P 500 reached an all-time high, driven by strong tech sector performance.", "title": "S&P 500 hits record high", "description": "Positive"},
    
    # Negative cases
    {"article_text": "Bitcoin dropped 15% amid regulatory concerns in the US.", "title": "Bitcoin falls on regulatory fears", "description": "Negative"},
    {"article_text": "Tesla stock plunged after the company missed delivery targets.", "title": "Tesla shares drop after weak sales", "description": "Negative"},
    {"article_text": "A massive crypto hack resulted in the loss of $500 million in digital assets.", "title": "Crypto exchange hacked", "description": "Negative"},
    {"article_text": "The Federal Reserve's interest rate hike led to a sharp decline in the stock market.", "title": "Markets tumble after Fed decision", "description": "Negative"},
    {"article_text": "Ethereum gas fees spiked to record highs, frustrating traders.", "title": "Ethereum fees skyrocket", "description": "Negative"},
    
    # Neutral cases
    {"article_text": "Bitcoin remained stable around $40,000, with little movement in the past week.", "title": "Bitcoin holds steady", "description": "Neutral"},
    {"article_text": "The stock market saw mixed results today, with some sectors gaining while others declined.", "title": "Markets end mixed", "description": "Neutral"},
    {"article_text": "Ethereum developers announced plans for the next network upgrade, but details remain unclear.", "title": "Ethereum team discusses future plans", "description": "Neutral"},
    {"article_text": "Gold and crypto have shown similar trends in recent months, according to analysts.", "title": "Gold vs. crypto trends", "description": "Neutral"},
    {"article_text": "Apple stock saw slight fluctuations throughout the day but ended unchanged.", "title": "Apple stock remains flat", "description": "Neutral"}
    ]


    for i, test_case in enumerate(test_cases, start=1):
        print(f"Test {i}: {test_case['description']}")
        pred = predict_sentiment(test_case["article_text"], test_case["title"])
        print(f"Predicted Sentiment Score: {pred}")
