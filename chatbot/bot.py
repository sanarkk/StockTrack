import os
import boto3
import uvicorn
import asyncio
import threading


from typing import Dict
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from telegram import Update, Message
from passlib.context import CryptContext
from telegram.ext import (
    Application,
    Updater,
    filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
)
from mypy_boto3_dynamodb.type_defs import (
    TableAttributeValueTypeDef,
    PutItemOutputTableTypeDef,
)
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

dotenv_path = os.path.join(os.path.dirname(__file__), "../backend/.env")
load_dotenv(dotenv_path)

AWS_REGION = os.getenv("AWS_REGION", "")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
USERS_TABLE = os.getenv("USERS_TABLE", "users")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
USERNAME, PASSWORD = range(2)

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

app = FastAPI()  # This is your main backend
users_table = dynamodb.Table(USERS_TABLE)
bot = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageRequest(BaseModel):
    chat_id: str
    article: dict


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_username(
    username: str,
) -> Dict[str, TableAttributeValueTypeDef] | str | bool | None:
    try:
        response = users_table.query(
            IndexName="username-index",
            KeyConditionExpression=Key("username").eq(username),
        )
        if "Items" in response and len(response["Items"]) > 0:
            user_item = response["Items"][0]  # Get the first matching item
            return user_item
        else:
            return False
    except ClientError as e:
        print(f"Error updating DynamoDB: {e}")


def assign_chat_to_user(username: str, chat_id: str) -> None:
    user = get_user_by_username(username)
    if user:
        try:
            user_id = user["user_id"]
            response = users_table.update_item(
                Key={"user_id": user_id},
                UpdateExpression="SET chat_id = :chat_id",
                ExpressionAttributeValues={":chat_id": chat_id},
                ReturnValues="UPDATED_NEW",
            )
        except ClientError as e:
            print(f"Error updating DynamoDB: {e}")


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! Please enter you username.")
    return USERNAME


async def get_username(update: Update, context: CallbackContext):
    username = update.message.text
    context.user_data["username"] = username
    await update.message.reply_text("Now, please enter your password.")
    return PASSWORD


async def get_password(update: Update, context: CallbackContext):
    password = update.message.text
    username = context.user_data.get("username")
    user = get_user_by_username(username)
    if not user or not verify_password(str(password), str(user["password"])):
        await update.message.reply_text(
            "Invalid username or password. Please try again."
        )
        return USERNAME

    assign_chat_to_user(username, str(update.message.chat_id))
    await update.message.reply_text(
        f"Hello {username}, you're successfully logged in!"
    )

    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Authentication canceled.")
    return ConversationHandler.END


@app.post("/send_telegram_message/")
async def send_message(request: MessageRequest):
    print("HEREERE")
    try:
        print("HEREERE")
        try:
            print("HEREERE")
            result = await bot.bot.send_message(
                chat_id=request.chat_id, text=request.article
            )
            print("HEREERE")
            print("message was sent")
        except Exception as e:
            print(e)
        return {"status": "Message sent successfully"}
    except Exception as e:
        return {"error": str(e)}


def run_app():
    uvicorn.run(app, host="0.0.0.0", port=8004)


def run_bot():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            USERNAME: [MessageHandler(filters.TEXT, get_username)],
            PASSWORD: [MessageHandler(filters.TEXT, get_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    bot.add_handler(conv_handler)
    loop = asyncio.get_event_loop()
    loop.create_task(bot.run_polling(allowed_updates=Update.ALL_TYPES))
    print("sdfsdfsdf")


if __name__ == "__main__":
    fastapi_thread_1 = threading.Thread(target=run_app)
    fastapi_thread_1.start()

    run_bot()
