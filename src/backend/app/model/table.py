from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String(100), primary_key=True)  # 文字数を増やす
    game_name = Column(String(50), nullable=False)
    tag_line = Column(String(10), nullable=False)


class Match(Base):
    __tablename__ = "matches"
    id = Column(String(50), primary_key=True)
    puuid = Column(String(50), nullable=False)
    map_name = Column(String(50), nullable=False)
    game_mode = Column(String(50), nullable=False)
    score = Column(Integer, nullable=False)
    kills = Column(Integer, nullable=False)
    deaths = Column(Integer, nullable=False)
    assists = Column(Integer, nullable=False)
    headshot_percentage = Column(Float, nullable=False)
    user_id = Column(String(26), ForeignKey('users.id'))

    user = relationship("User")

class MatchComment(Base):
    __tablename__ = "match_comments"
    id = Column(String(50), primary_key=True)
    match_id = Column(String(50), ForeignKey('matches.id'))
    comment = Column(String(255), nullable=True)

    match = relationship("Match")
