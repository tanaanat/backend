from fastapi import FastAPI,Body
from pydantic import BaseModel
from fastapi import HTTPException
from .app.database.database import read_table  #インポートする時 "."を前に着ける
from .app.database.database import read_id
from fastapi.middleware.cors import CORSMiddleware
from .app.database.database import delete_user
from .app.model.table import User
from .app.database.database import create_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}



@app.get("/database")
def read_user(): 
    return read_table()
    #datebase と名前変える

@app.get("/users/{id}")
def getuser_id(id:int): 
    return read_id(id)

# ユーザー追加エンドポイント（POSTメソッド）
@app.post("/post")
def create_users(id: int = Body(...),name: str = Body(...),age: str = Body(...)):
    user=User(id=id,name=name,age=age)  
    create_user(user)
    return create_user(user)

# ユーザー削除エンドポイント（DELETEメソッド）
# @app.delete("/delete/{id}")
# def delete_userid(id:int):
#     delete_user(id)
#     result = delete_user(id)  # 実際に削除する処理
#     if not result:
#         raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
#     return{"message": f"ユーザー {id} が削除されました"}

@app.delete("/delete/{id}")
def delete_userid(id:int):
    return delete_user(id)