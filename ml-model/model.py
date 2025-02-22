import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import scipy.sparse as sp
import numpy as np
import joblib
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

def preprocess_text(text):
    text = text.lower()
    return text

def train_sentiment_model(data_path):
    print("Loading dataset...")
    df = pd.read_csv(data_path)
    print("Dataset loaded. Shape:", df.shape)

    print("Dropping missing values...")
    df = df.dropna(subset=['article_content', 'sentiment_score'])
    print("Dataset shape after dropping missing values:", df.shape)

    print("Preprocessing text...")
    df['article_content'] = df['article_content'].apply(preprocess_text)

    print("Vectorizing text data...")
    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
    X_text_vectorized = vectorizer.fit_transform(df['article_content'])
    print("Text vectorization complete. Shape:", X_text_vectorized.shape)

    print("Scaling sentiment scores...")
    X_sentiment = df[['sentiment_score']].values
    scaler = StandardScaler()
    X_sentiment = scaler.fit_transform(X_sentiment)

    print("Combining features...")
    X = sp.hstack((X_text_vectorized, X_sentiment), format='csr')
    y = df['sentiment_score']
    print("Feature matrix shape:", X.shape, "Target shape:", y.shape)

    print("Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training RandomForestRegressor...")
    model = RandomForestRegressor(n_estimators=200, max_depth=None, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print("Model evaluation complete. MSE:", mse)

    return model, vectorizer, scaler, mse

def predict_sentiment(model, vectorizer, scaler, new_article_text, sentiment_score):
    print("Processing new input for prediction...")
    new_text_vectorized = vectorizer.transform([preprocess_text(new_article_text)])
    new_sentiment_scaled = scaler.transform(np.array([[sentiment_score]]))
    new_X = sp.hstack((new_text_vectorized, new_sentiment_scaled), format='csr')
    print("Feature vector for prediction prepared. Shape:", new_X.shape)
    prediction = model.predict(new_X)
    print("Prediction complete.")
    return prediction

data_path = 'preprocessed_data.csv'
print("Starting training process...")
model, vectorizer, scaler, mse = train_sentiment_model(data_path)
print("Training process completed.")

new_article_text = "Apple Inc. announced record-breaking profits this quarter."
sentiment_score = 0.95
print("Making prediction for new article...")
prediction = predict_sentiment(model, vectorizer, scaler, new_article_text, sentiment_score)
print("Predicted Sentiment Score:", prediction[0])

print("Saving model, vectorizer, and scaler...")
joblib.dump(model, 'sentiment_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
joblib.dump(scaler, 'sentiment_scaler.pkl')
print("Model, vectorizer, and scaler saved to disk.")