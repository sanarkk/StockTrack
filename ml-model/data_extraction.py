import pandas as pd
from transformers import pipeline
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

load_dotenv()

def read_latest_processed_index():
    try:
        df = pd.read_csv("preprocessed_data.csv", usecols=["index_key"])
        if not df.empty:
            return df["index_key"].max()
    except FileNotFoundError:
        print("No existing preprocessed data found. Starting fresh.")
    return None

def read_new_data_from_database(last_index_key):
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.getenv("AWS_REGION_NAME"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    table = dynamodb.Table('InsiderArticles')

    try:
        response = table.scan()
        items = response['Items']
        df = pd.DataFrame(items)

        if df.empty:
            print("No data found in DynamoDB.")
            return df

        df["index_key"] = df["index_key"].astype(int)

        if last_index_key is not None:
            last_index_key = int(last_index_key)
            df = df[df["index_key"] > last_index_key]

        print(f"Found {len(df)} new records in DynamoDB.")
        return df
    except ClientError as e:
        print("Error reading from DynamoDB:", e)
        return pd.DataFrame()

def get_sentiments(articles):
    print("Starting sentiment analysis...")
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    results = []
    for i, article in enumerate(articles):
        print(f"Analyzing sentiment for article {i + 1}/{len(articles)}...")
        result = sentiment_pipeline(article[:512])[0]
        results.append({"label": result['label'], "score": result['score']})
    print("Sentiment analysis complete.")
    return results

def summarize_articles(articles):
    print("Starting summarization...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summaries = []
    for i, article in enumerate(articles):
        print(f"Summarizing article {i + 1}/{len(articles)}...")
        summary = summarizer(article[:1024], max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    print("Summarization complete.")
    return summaries

def analyze_articles(articles):
    print("Starting detailed analysis...")
    analysis_pipeline = pipeline("text-generation", model="gpt2")
    analyses = []
    for i, article in enumerate(articles):
        print(f"Analyzing article {i + 1}/{len(articles)}...")
        # Directly generate analysis without additional text
        analysis = analysis_pipeline(article[:512], max_length=200, num_return_sequences=1)[0]['generated_text']
        analyses.append(analysis)
    print("Detailed analysis complete.")
    return analyses

def preprocess_data():
    print("Starting data preprocessing...")

    last_index_key = read_latest_processed_index()
    print(f"Last processed index: {last_index_key}")

    new_data = read_new_data_from_database(last_index_key)

    if new_data.empty:
        print("No new data found. Exiting.")
        return

    print(f"Processing {len(new_data)} new articles...")

    print("Performing sentiment analysis...")
    sentiments = get_sentiments(new_data['article_text'].tolist())
    new_data['sentiment'] = [s['label'] for s in sentiments]
    new_data['sentiment_score'] = [s['score'] for s in sentiments]

    print("Performing summarization...")
    new_data['summary'] = summarize_articles(new_data['article_text'].tolist())

    print("Performing detailed analysis...")
    new_data['analysis'] = analyze_articles(new_data['article_text'].tolist())

    print("Appending new data to CSV...")
    new_data.to_csv("preprocessed_data.csv", mode='a', header=not os.path.exists("preprocessed_data.csv"), index=False)

    print(f"Processed {len(new_data)} new articles and appended to 'preprocessed_data.csv'.")
    print("Preprocessing complete.")

if __name__ == "__main__":
    preprocess_data()