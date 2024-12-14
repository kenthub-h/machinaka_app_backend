# generate_password_hash.py
from passlib.context import CryptContext

# パスワードをハッシュ化するための設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 各ユーザーのパスワード
passwords = {
    1: "1111",
    2: "2222",
    3: "3333",
    4: "4444",
    5: "5555"
}

# ハッシュ化されたパスワードを生成
hashed_passwords = {user_id: pwd_context.hash(password) for user_id, password in passwords.items()}

# 結果を表示
for user_id, hashed_password in hashed_passwords.items():
    print(f"user_id: {user_id}, hashed_password: {hashed_password}")
