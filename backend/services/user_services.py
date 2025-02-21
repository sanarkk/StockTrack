import uuid

from typing import Dict
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.type_defs import (
    TableAttributeValueTypeDef,
    PutItemOutputTableTypeDef,
)

from database.dynamodb import users_table
from config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY


def get_user_by_username(
    username: str,
) -> Dict[str, TableAttributeValueTypeDef] | str | bool | None:
    try:
        response = users_table.query(
            IndexName="username-index",
            KeyConditionExpression=Key("username").eq(username),
        )
        if "Items" in response and len(response["Items"]) > 0:
            user_item = response["Items"][0]
            return user_item
        else:
            return False
    except ClientError as ce:
        print(f"Error updating DynamoDB: {ce}")


def create_user(
    user_data: dict,
) -> PutItemOutputTableTypeDef:
    user_id = str(uuid.uuid4())
    user_data["user_id"] = user_id
    response = users_table.put_item(Item=user_data)
    return response


def assign_chat_to_user(username: str, chat_id: str) -> None:
    user = get_user_by_username(username)
    if user:
        try:
            user_id = user["id"]
            response = users_table.update_item(
                Key={"id": user_id},
                UpdateExpression="SET chat_id = :chat_id",
                ExpressionAttributeValues={":chat_id": chat_id},
                ReturnValues="UPDATED_NEW",
            )
        except ClientError as e:
            print(f"Error updating DynamoDB: {e}")
