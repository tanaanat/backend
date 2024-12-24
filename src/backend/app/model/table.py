from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from ulid import ulid

from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String(26), primary_key=True)
    username = Column(String(255), nullable=False, unique=True)

    def __init__(self, username: str):
        self.id = str(ulid())
        self.username = username

class Map(Base):
    __tablename__ = "maps"
    id = Column(String(26), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    def __init__(self, name: str):
        self.id = str(ulid())
        self.name = name

class Character(Base):
    __tablename__ = "characters"
    id = Column(String(26), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    def __init__(self, name: str):
        self.id = str(ulid())
        self.name = name

class Stat(Base):
    __tablename__ = "stats"
    id = Column(String(26), primary_key=True)
    user_id = Column(String(26), ForeignKey('users.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    map_id = Column(String(26), ForeignKey('maps.id'), nullable=False)
    character_id = Column(String(26), ForeignKey('characters.id'), nullable=False)
    acs = Column(Integer, nullable=False)
    kills = Column(Integer, nullable=False)
    deaths = Column(Integer, nullable=False)
    assists = Column(Integer, nullable=False)
    headshot_percentage = Column(Float, nullable=False)
    first_kills = Column(Integer, nullable=False)
    first_deaths = Column(Integer, nullable=False)
    multi_kills = Column(Integer, nullable=False)
    memo = Column(String(255))

    def __init__(self, user_id: str, map_id: str, character_id: str, acs: int, kills: int, deaths: int, 
                 assists: int, headshot_percentage: float, first_kills: int, first_deaths: int, 
                 multi_kills: int, memo: str = None):
        self.id = str(ulid())
        self.user_id = user_id
        self.map_id = map_id
        self.character_id = character_id
        self.acs = acs
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.headshot_percentage = headshot_percentage
        self.first_kills = first_kills
        self.first_deaths = first_deaths
        self.multi_kills = multi_kills
        self.memo = memo
