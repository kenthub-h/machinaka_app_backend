from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

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

