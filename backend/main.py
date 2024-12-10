# main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from pydantic import EmailStr
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from database import test_connection, engine, get_db, SessionLocal  # DB関連のモジュールをインポート
from models import User # ログイン用
from sqlalchemy import text
from sqlalchemy.orm import Session # ログイン用
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt #JWTトークン
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

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

# # 仮のユーザー情報
# mock_user = {
#     "email": "machinaka@tribiz.jp",
#     "password": pwd_context.hash("123456"),  # パスワードをハッシュ化して保存
# }

# ユーザーログイン用のモデル
class UserLogin(BaseModel):
    email: EmailStr  # メールアドレス形式を強制
    password: str

# .envファイルを読み込む。環境変数とアルゴリズム設定
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")  # トークンの署名に使う秘密鍵（安全な場所に保管）
ALGORITHM = "HS256"  # トークンの署名アルゴリズム（一般的にHS256）
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # トークンの有効期限（分）

# トークン作成関数
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ログインエンドポイント
@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    # データベースからユーザーを取得
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="メールアドレスまたはパスワードが間違っています。")
    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="メールアドレスまたはパスワードが間違っています。")

    # トークンの発行
    token_data = {"user_id": db_user.user_id, "email": db_user.email}
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer", "user_name": db_user.user_name}

# OAuth2PasswordBearer設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# トークン検証関数
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="トークンが無効です。")
        user = db.query(User).filter(User.user_id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません。")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="トークンが無効です。")


# # ログインエンドポイント（DB仕様前）
# @app.post("/login")
# async def login(user: UserLogin):
#     # ユーザー情報を確認
#     if user.email == mock_user["email"]:
#         if pwd_context.verify(user.password, mock_user["password"]):
#             return {"message": "ログイン成功"}
#         else:
#             raise HTTPException(status_code=401, detail="パスワードが間違っています。")
#     raise HTTPException(status_code=404, detail="メールアドレスが見つかりません。")

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

# 認証されたエンドポイントの例
@app.get("/profile")
async def read_profile(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.user_id, "user_name": current_user.user_name, "email": current_user.email}

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

# DBセッションの取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
