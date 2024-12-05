# reset_db.py
from database import Base, engine
import models  # モデルを明示的にインポート

def reset_database():
    # 既存のテーブルを削除
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped.")

    # 新しいテーブルを作成
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")

if __name__ == "__main__":
    reset_database()
