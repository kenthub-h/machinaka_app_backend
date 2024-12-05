from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from database import test_connection #モギ追加：DBモジュール
from sqlalchemy import text  #モギ追加
from database import engine  # モギ追加：engineをインポート

app = FastAPI()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では特定のオリジンのみ許可してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# パスワードのハッシュ化設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 仮のユーザー情報
mock_user = {
    "email": "machinaka@tribiz.jp",
    "password": pwd_context.hash("123456"),  # パスワードをハッシュ化して保存
}

# ユーザーログイン用のモデル
class UserLogin(BaseModel):
    email: str
    password: str

# ログインエンドポイント
@app.post("/login")
async def login(user: UserLogin):
    # ユーザー情報を確認
    if user.email == mock_user["email"]:
        if pwd_context.verify(user.password, mock_user["password"]):
            return {"message": "ログイン成功"}
        else:
            raise HTTPException(status_code=401, detail="パスワードが間違っています。")
    raise HTTPException(status_code=404, detail="メールアドレスが見つかりません。")

#モギ追加：DB接続テスト
@app.on_event("startup")
def startup_event():
    # データベース接続テストを実行
    test_connection()

@app.get("/test-db-connection")
def test_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE()"))
            db_name = result.fetchone()[0] if result.rowcount > 0 else "No database selected"
            return {"message": "Connected to database", "database": db_name}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}