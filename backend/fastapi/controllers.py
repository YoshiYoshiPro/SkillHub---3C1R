from typing import List

import uvicorn
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from core.database import get_db  # ここでget_db関数をインポート
from crud import crud
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from migration import models
from schemas import schemas

'''from core import config
from crud import crud'''


# from migration import database, models

app = FastAPI(title="社内勉強会の開催を活発にするwebアプリ", description="社内の勉強会の予定を共有するWebアプリケーション")


router = APIRouter()

# CORS対応 (https://qiita.com/satto_sann/items/0e1f5dbbe62efc612a78)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def index(request: Request):
    return {"Hello": "World"}


def get_data(request: Request):
    return {"key": "value", "message": "Hello from FastAPI!"}


def get_tag_result(request: Request, tag):
    return {
        "is_accepted": True,
        "interests": [
            {
                "user_id": tag,
                "name": tag,
                "icon_url": "http://localhost:3000/logo192.png",
            },
            {
                "user_id": "bbb",
                "name": "いいい",
                "icon_url": "http://localhost:3000/logo192.png",
            },
            {
                "user_id": "ccc",
                "name": "ううう",
                "icon_url": "http://localhost:3000/logo192.png",
            },
        ],
        "expertises": [
            {
                "user_id": "ccc",
                "name": "ううう",
                "icon_url": "http://localhost:3000/logo192.png",
                "years": 8,
            },
            {
                "user_id": "ddd",
                "name": "えええ",
                "icon_url": "http://localhost:3000/logo192.png",
                "years": 13,
            },
        ],
        "experiences": [
            {
                "user_id": "aaa",
                "name": "あああ",
                "icon_url": "http://localhost:3000/logo192.png",
                "years": 1,
            },
            {
                "user_id": "bbb",
                "name": "いいい",
                "icon_url": "http://localhost:3000/logo192.png",
                "years": 2,
            },
            {
                "user_id": "ccc",
                "name": "ううう",
                "icon_url": "http://localhost:3000/logo192.png",
                "years": 8,
            },
            {
                "user_id": "ddd",
                "name": "えええ",
                "icon_url": "http://localhost:3000/logo192.png",
                "years": 13,
            },
            {
                "user_id": "eee",
                "name": "おおお",
                "icon_url": "http://localhost:3000/logo192.png",
                "years": 5,
            },
        ],
    }


def get_suggested_tags(request: Request, tag_substring):
    tmp_tags = ["Java", "JavaScript", "SolidJS", "Three.JS", "Golang"]

    return {
    	"suggested_tags": [tag for tag in tmp_tags if tag_substring in tag],
    }

def get_user_by_id(request: Request, user_id: int):
    # データベースセッションを取得
    db = request.state.db

    # ユーザーをデータベースから取得
    user = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def create_user(user: schemas.UsersCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


def get_all_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)  # データベース操作関数を呼び出してデータを取得
    return users
