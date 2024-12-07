# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from database import test_connection, engine  # DB関連のモジュールをインポート
from sqlalchemy import text

# 各ルーターをインポート
from routers import offices, users, projects, skills, industries, job_titles

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

# データベース接続テストをスタートアップイベントに設定
@app.on_event("startup")
def startup_event():
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

# 各ルーターを登録
app.include_router(offices.router, prefix="/api", tags=["offices"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(projects.router, prefix="/api", tags=["projects"])
app.include_router(skills.router, prefix="/api", tags=["skills"])
app.include_router(industries.router, prefix="/api", tags=["industries"])
app.include_router(job_titles.router, prefix="/api", tags=["job_titles"])

# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "Welcome to the Machinaka App API"}