import requests
from fastapi import FastAPI, Body,HTTPException,Request, Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .app.database.database import session
from .app.model.table import User, Match, MatchComment
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
app = FastAPI()

# 静的ファイルを提供（favicon.ico対応）
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join("static", "favicon.ico"))

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        session.commit()  # 明示的にトランザクションを終了
    except Exception as e:
        session.rollback()  # エラー時にロールバック
        print(f"Database error: {e}")
        raise
    finally:
        session.close()  # 必ずセッションを閉じる
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], ##http://172.22.91.9:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RIOT_API_KEY = "RGAPI-9f0ccbfa-ac89-4a86-a1c8-02543af81c20"  # APIキーを.envに管理推奨

class RiotAccount(BaseModel):
    gameName: str
    tagLine: str

class MatchCommentRequest(BaseModel):
    match_id: str
    comment: str


@app.get("/")
def root():
    return {"message": "Server is running"}

    
# プレイヤー情報取得エンドポイント
@app.post("/riot/account")
def get_riot_account(account: RiotAccount):
    url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{account.gameName}/{account.tagLine}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        try:
            # 既存のユーザーを確認
            existing_user = session.query(User).filter_by(id=data['puuid']).first()
            if existing_user is None:
                new_user = User(
                    id=data['puuid'],
                    game_name=account.gameName,
                    tag_line=account.tagLine
                )
                session.add(new_user)
                session.commit()
                print("User added to the database")
            else:
                print("User already exists")

            return data
        except Exception as e:
            session.rollback()  # トランザクションをロールバック
            print("Database transaction error:", e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve account information")

# 試合履歴取得エンドポイント
@app.get("/riot/matches/{puuid}")
def get_match_history(puuid: str):
    url = f"https://americas.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        match_data = response.json()
        for match in match_data['history']:
            new_match = Match(id=match['matchId'], puuid=puuid, map_name="Unknown", game_mode="Unknown",
                              score=0, kills=0, deaths=0, assists=0, headshot_percentage=0.0)
            session.add(new_match)
        session.commit()
        return match_data
    else:
        return {"error": "Failed to retrieve match history"}

# コメント追加エンドポイント
@app.post("/match/comment")
def add_match_comment(request: MatchCommentRequest):
    new_comment = MatchComment(match_id=request.match_id, comment=request.comment)
    session.add(new_comment)
    session.commit()
    return {"message": "Comment added successfully"}

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        response = await call_next(request)
    except Exception as e:
        session.rollback()  # すべての例外に対してロールバックを実行
        print(f"Database rollback due to error: {e}")
    finally:
        session.close()  # セッションを確実に閉じる
    return response