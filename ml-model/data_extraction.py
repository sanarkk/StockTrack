import pandas as pd
from transformers import pipeline
import boto3
import csv
from decimal import Decimal
import uuid
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_REGION_NAME"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
processed_articles_table = dynamodb.Table("ProcessedArticles")


class Article(BaseModel):
    url: str
    title: str
    publish_date: str
    article_text: str
    stock_ticker: str
    news_source: str
    index_key: int
    parsing_date: str


def get_sentiment(article_text):
    print("Starting sentiment analysis...")
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
    )
    result = sentiment_pipeline(article_text[:512])[0]
    print("Sentiment analysis complete.")
    return {"label": result["label"], "score": result["score"]}


def summarize_article(article_text):
    print("Starting summarization...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(
        article_text[:1024], max_length=150, min_length=30, do_sample=False
    )[0]["summary_text"]
    print("Summarization complete.")
    return summary


def analyze_article(article_text):
    print("Starting detailed analysis...")
    analysis_pipeline = pipeline("text-generation", model="gpt2")
    analysis = analysis_pipeline(
        article_text[:512], max_length=200, num_return_sequences=1
    )[0]["generated_text"]
    print("Detailed analysis complete.")
    return analysis


@app.post("/process_article/")
def process_article(article: Article):
    print("Starting article processing...")

    # Parse the input JSON
    # Perform sentiment analysis, summarization, and detailed analysis
    sentiment = get_sentiment(article.article_text)
    summary = summarize_article(article.article_text)
    analysis = analyze_article(article.article_text)

    article = article.dict()
    # Add processed fields to the article
    article["sentiment"] = sentiment["label"]
    article["sentiment_score"] = Decimal(str(sentiment["score"]))
    article["summary"] = summary
    article["analysis"] = analysis
    article["id"] = str(uuid.uuid4())

    # Append new processed data to the file
    processed_articles_table.put_item(Item=article)
    print("Preprocessing complete.")


def run_app():
    uvicorn.run(app, host="0.0.0.0", port=8006)


if __name__ == "__main__":
    run_app()
