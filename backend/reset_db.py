# reset_db.py
from database import Base, engine
import models  # モデルを明示的にインポート
from sqlalchemy.schema import CreateTable

def reset_database():
    print(f"Connected to database: {engine.url.database}")
    # 既存のテーブルを削除
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped.")

    # 新しいテーブルを作成
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")
    # 実際に発行されているSQLを表示
    for table in Base.metadata.sorted_tables:
        print(str(CreateTable(table)))

if __name__ == "__main__":
    reset_database()
