import pandas as pd
from transformers import pipeline
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def read_latest_processed_index():
    """
    Read the latest processed index from the CSV file.
    """
    try:
        df = pd.read_csv("preprocessed_data.csv", usecols=["index_key"])
        if not df.empty:
            return df["index_key"].max()  # Get the latest processed index
    except FileNotFoundError:
        print("No existing preprocessed data found. Starting fresh.")
    return None  # No previous data found

def read_new_data_from_database(last_index_key):
    """
    Fetch only new data from the DynamoDB table based on the last processed index.
    """
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
            return df

        df["index_key"] = df["index_key"].astype(int)

        if last_index_key is not None:
            last_index_key = int(last_index_key)
            df = df[df["index_key"] > last_index_key]

        return df
    except ClientError as e:
        print("Error reading from DynamoDB:", e)
        return pd.DataFrame()


def get_sentiments(articles):
    """
    Analyze sentiment of articles using Hugging Face pipeline.
    """
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    return [{"label": sentiment_pipeline(article[:512])[0]['label'], "score": sentiment_pipeline(article[:512])[0]['score']} for article in articles]

def summarize_articles(articles):
    """
    Summarize articles using Hugging Face pipeline.
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return [summarizer(article[:1024], max_length=150, min_length=30, do_sample=False)[0]['summary_text'] for article in articles]

def analyze_articles(articles):
    """
    Generate detailed analysis of articles using Hugging Face pipeline.
    """
    analysis_pipeline = pipeline("text-generation", model="gpt2")
    return [analysis_pipeline(f"Provide a detailed analysis:\n\n{article[:512]}\n\nAnalysis:", max_length=200, num_return_sequences=1)[0]['generated_text'] for article in articles]

def preprocess_data():
    """
    Preprocess the data: Fetch new data, process it, and append only new records.
    """
    print("Starting data preprocessing...")

    last_index_key = read_latest_processed_index()
    print(f"Last processed index: {last_index_key}")

    new_data = read_new_data_from_database(last_index_key)

    if new_data.empty:
        print("No new data found. Exiting.")
        return

    print(f"Processing {len(new_data)} new articles...")

    # Perform sentiment analysis, summarization, and detailed analysis on new records
    sentiments = get_sentiments(new_data['article_text'].tolist())
    new_data['sentiment'] = [s['label'] for s in sentiments]
    new_data['sentiment_score'] = [s['score'] for s in sentiments]
    new_data['summary'] = summarize_articles(new_data['article_text'].tolist())
    new_data['analysis'] = analyze_articles(new_data['article_text'].tolist())

    # Append new processed data to the file
    new_data.to_csv("preprocessed_data.csv", mode='a', header=not os.path.exists("preprocessed_data.csv"), index=False)

    print(f"Processed {len(new_data)} new articles and appended to 'preprocessed_data.csv'.")
    print("Preprocessing complete.")

if __name__ == "__main__":
    preprocess_data()
