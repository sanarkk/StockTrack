import boto3
from config import (
    USERS_TABLE,
    POSTS_TABLE,
    AWS_REGION,
    AWS_ACCESS_KEY,
    AWS_SECRET_ACCESS_KEY,
)

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

users_table = dynamodb.Table(USERS_TABLE)
