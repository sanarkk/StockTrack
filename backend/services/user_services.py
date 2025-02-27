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
            latest_user = users_table.get_item(
                Key={"user_id": user_item["user_id"]},
                ConsistentRead=True,
            )
            try:
                interested_in = latest_user["Item"].get("interested_in")
            except KeyError as e:
                interested_in = []
            if not interested_in or len(interested_in) == 0:
                interested_in = []
            result = {
                "user_id": user_item["user_id"],
                "username": user_item.get("username"),
                "password": user_item.get("password"),
                "interested_in": (
                    interested_in
                    if interested_in and len(interested_in) > 0
                    else []
                ),
            }
            return result
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
