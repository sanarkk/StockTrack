import pandas as pd
from transformers import pipeline
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
import uuid
import csv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "../backend/.env")
load_dotenv(dotenv_path)

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
processed_articles_table = dynamodb.Table("ProcessedArticles")


def read_database_data():
    """
    Fetch data from DynamoDB table.
    """

    table = dynamodb.Table("InsiderArticles")
    try:
        response = table.scan()
        items = response["Items"]
        return pd.DataFrame(items)[:10]
    except ClientError as e:
        print("Error reading from DynamoDB:", e)
        return pd.DataFrame()


def get_sentiments(articles):
    """
    Analyze sentiment of articles using Hugging Face pipeline.
    """
    print("Analyzing sentiment for articles...")
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
    )
    sentiments = []
    for i, article in enumerate(articles):
        if article:
            try:
                print(
                    f"Analyzing sentiment for article {i + 1}/{len(articles)}..."
                )
                sentiment = sentiment_pipeline(article[:512])[0]
                sentiments.append(sentiment)
            except Exception as e:
                print(f"Error analyzing sentiment for article {i + 1}: {e}")
                sentiments.append({"label": "NEUTRAL", "score": 0.0})
        else:
            print(f"Article {i + 1} is empty or could not be fetched.")
            sentiments.append({"label": "NEUTRAL", "score": 0.0})
    print("Finished sentiment analysis.")
    return sentiments


def summarize_articles(articles):
    """
    Summarize articles using Hugging Face pipeline.
    """
    print("Summarizing articles...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summaries = []
    for i, article in enumerate(articles):
        if article:
            try:
                print(f"Summarizing article {i + 1}/{len(articles)}...")
                summary = summarizer(
                    article[:1024],
                    max_length=150,
                    min_length=30,
                    do_sample=False,
                )[0]["summary_text"]
                summaries.append(summary)
            except Exception as e:
                print(f"Error summarizing article {i + 1}: {e}")
                summaries.append("Summary unavailable.")
        else:
            print(f"Article {i + 1} is empty or could not be fetched.")
            summaries.append("Summary unavailable.")
    print("Finished summarizing articles.")
    return summaries


def analyze_articles(articles):
    """
    Generate detailed analysis of articles using Hugging Face pipeline.
    """
    print("Analyzing articles...")
    analysis_pipeline = pipeline("text-generation", model="gpt2")
    analyses = []
    for i, article in enumerate(articles):
        if article:
            try:
                print(f"Analyzing article {i + 1}/{len(articles)}...")
                prompt = f"Provide a detailed analysis of the following article:\n\n{article[:512]}\n\nAnalysis:"
                analysis = analysis_pipeline(
                    prompt, max_length=200, num_return_sequences=1
                )[0]["generated_text"]
                analyses.append(analysis)
            except Exception as e:
                print(f"Error analyzing article {i + 1}: {e}")
                analyses.append("Analysis unavailable.")
        else:
            print(f"Article {i + 1} is empty or could not be fetched.")
            analyses.append("Analysis unavailable.")
    print("Finished analyzing articles.")
    return analyses


def preprocess_data():
    """
    Preprocess the data: fetch, analyze, and save results.
    """
    print("Starting data preprocessing...")
    data = read_database_data()
    print("Dataset loaded. Shape:", data.shape)

    if data.empty:
        print("No data found. Exiting.")
        return

    # Perform sentiment analysis, summarization, and detailed analysis
    data["sentiment"] = [
        s["label"] for s in get_sentiments(data["article_text"].tolist())
    ]
    data["sentiment_score"] = [
        s["score"] for s in get_sentiments(data["article_text"].tolist())
    ]
    data["summary"] = summarize_articles(data["article_text"].tolist())
    data["analysis"] = analyze_articles(data["article_text"].tolist())

    # Save preprocessed data with all columns
    print("Saving preprocessed data to 'preprocessed_data.csv'...")
    data.to_csv("preprocessed_data.csv", index=False)
    with open("preprocessed_data.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # Read as dictionary
        for row in reader:
            row["id"] = str(uuid.uuid4())
            processed_articles_table.put_item(Item=row)
    # Generate data overview
    print("Generating data overview...")
    generate_data_overview(data)

    print(
        "Preprocessing complete. Data saved to 'preprocessed_data.csv' and overview saved to 'data_overview.txt'."
    )

    print("\nHead of the preprocessed data:")
    print(data.head())


def generate_data_overview(data):
    """
    Generate a text overview of the dataset.
    """
    overview = []
    overview.append("=== Dataset Overview ===")
    overview.append(f"Total Rows: {len(data)}")
    overview.append(f"Columns: {', '.join(data.columns)}")
    overview.append("\n=== Sentiment Distribution ===")
    sentiment_distribution = data["sentiment"].value_counts()
    overview.append(sentiment_distribution.to_string())
    overview.append("\n=== Sentiment Score Statistics ===")
    sentiment_score_stats = data["sentiment_score"].describe()
    overview.append(sentiment_score_stats.to_string())
    overview.append("\n=== Sample Data ===")
    overview.append(data.head().to_string())
    with open("data_overview.txt", "w") as f:
        f.write("\n".join(overview))


if __name__ == "__main__":
    preprocess_data()
