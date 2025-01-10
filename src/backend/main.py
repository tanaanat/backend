import requests
from fastapi import FastAPI, Body
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .app.database.database import session
from .app.model.table import User, Match, MatchComment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RIOT_API_KEY = "RGAPI-7383bee5-bd31-4810-863d-c8a255448c76"  # APIキーを.envに管理推奨

class RiotAccount(BaseModel):
    gameName: str
    tagLine: str

class MatchCommentRequest(BaseModel):
    match_id: str
    comment: str

# プレイヤー情報取得エンドポイント
@app.post("/riot/account")
def get_riot_account(account: RiotAccount):
    url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{account.gameName}/{account.tagLine}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        new_user = User(id=data['puuid'], game_name=account.gameName, tag_line=account.tagLine)
        session.add(new_user)
        session.commit()
        return data
    else:
        return {"error": "Failed to retrieve account information"}

# 試合履歴取得エンドポイント
@app.get("/riot/matches/{puuid}")
def get_match_history(puuid: str):
    url = f"https://asia.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}"
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
