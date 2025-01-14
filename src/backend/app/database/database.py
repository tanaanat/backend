from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# SupabaseのPostgresデータベースに接続
Engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

# セッションのエクスポート
session = SessionLocal()
