import { createClient } from '@supabase/supabase-js';
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import User

#環境変数からURLとキーを取得
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;

#Supabaseクライアントを作成
const supabase = createClient(supabaseUrl, supabaseKey);

export default supabase;

# Engine の作成
Engine = create_engine(
  DATABASE,
  echo=False
)

# Sessionの作成
session = Session(
  autocommit = False,
  autoflush = True,
  bind = Engine
)



def read_table():
    return session.query(User).all()

def read_id(id):
    return session.query(User).filter(User.id==id).first()
            

    
def create_user(user):
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def add_user(user):
    session.add(user)

def delete_user(id):
    return session.query(User).filter(User.id == id).delete()