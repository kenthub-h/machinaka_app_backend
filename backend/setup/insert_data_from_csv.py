# insert_data_from_csv
# insert_data_from_csv
import os
import pandas as pd
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text  # text() をインポート
from database import engine
from models import Office, User, Industry, JobTitle, Skill, Project

# カレントディレクトリをスクリプトのディレクトリに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# CSVフォルダパス
csv_folder_path = os.path.join("csv")

# CSVファイルをテーブルにマッピング（挿入順序を考慮）
csv_files = [
    ("offices.csv", Office),
    ("industries.csv", Industry),
    ("job_titles.csv", JobTitle),
    ("users.csv", User),
    ("skills.csv", Skill),
    ("projects.csv", Project),
]

# データ挿入関数
def insert_data_from_csv():
    try:
        with engine.connect() as connection:
            # 外部キー制約を一時的に無効化
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            print("Foreign key checks disabled.")

            for file_name, model in csv_files:
                file_path = os.path.join(csv_folder_path, file_name)
                # CSVデータ読み込み
                data = pd.read_csv(file_path)
                
                # 特定のテーブルに対する特別処理 (project_id は自動生成)
                if model.__tablename__ == "projects" and "project_id" in data.columns:
                    data = data.drop(columns=["project_id"])
                    print(f"`project_id` column dropped for table: {model.__tablename__}")

                # テーブルのデータを削除（DELETEを使用）
                connection.execute(text(f"DELETE FROM {model.__tablename__}"))
                print(f"Table {model.__tablename__} cleared successfully.")
                
                # データ挿入（既存データは保持せず置き換え）
                data.to_sql(
                    model.__tablename__,
                    con=connection,
                    if_exists="append",  # データを追加挿入
                    index=False
                )
                print(f"Data inserted successfully for table: {model.__tablename__}")

            # 外部キー制約を再度有効化
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            print("Foreign key checks enabled.")
    except IntegrityError as e:
        print(f"IntegrityError occurred: {e}")
    except Exception as e:
        print(f"Error occurred while inserting data: {e}")

if __name__ == "__main__":
    insert_data_from_csv()



# import os
# import pandas as pd
# from database import engine
# from models import Office, User, Industry, JobTitle, Skill, Project

# # カレントディレクトリをスクリプトのディレクトリに変更
# os.chdir(os.path.dirname(os.path.abspath(__file__)))

# # CSVフォルダパス
# csv_folder_path = os.path.join("csv")

# # CSVファイルをテーブルにマッピング
# csv_files = {
#     "offices.csv": Office,
#     "users.csv": User,
#     "industries.csv": Industry,
#     "job_titles.csv": JobTitle,
#     "skills.csv": Skill,
#     "projects.csv": Project,
# }

# # データ挿入
# def insert_data_from_csv():
#     try:
#         for file_name, model in csv_files.items():
#             file_path = os.path.join(csv_folder_path, file_name)
#             # CSV読み込みとデータ挿入
#             data = pd.read_csv(file_path)
#             with engine.connect() as connection:
#                 data.to_sql(model.__tablename__, con=connection, if_exists="replace", index=False) #append→replaceに変更（上書き）
#         print("Data insertion completed successfully!")
#     except Exception as e:
#         print(f"Error occurred while inserting data: {e}")

# if __name__ == "__main__":
#     insert_data_from_csv()




# import os
# import pandas as pd
# from sqlalchemy.orm import Session
# from database import engine, init_db
# from models import Office, User, Industry, JobTitle, Skill, Project

# csv_folder_path = os.path.join("backend", "csv")


# # CSVファイルのパスを設定
# CSV_DIR = "backend/csv"

# # テーブルごとのCSVファイル名
# CSV_FILES = {
#     "offices": "offices.csv",
#     "users": "users.csv",
#     "industries": "industries.csv",
#     "job_titles": "job_titles.csv",
#     "skills": "skills.csv",
#     "projects": "projects.csv",
# }

# # 各テーブルにデータを挿入
# def insert_data_from_csv():
#     session = Session(bind=engine)
    
#     try:
#         # Officesデータ
#         offices_path = os.path.join(CSV_DIR, CSV_FILES["offices"])
#         offices_data = pd.read_csv(offices_path, encoding="utf-8")  # UTF-8で読み込む
#         session.bulk_insert_mappings(Office, offices_data.to_dict(orient="records"))

#         # Usersデータ
#         users_path = os.path.join(CSV_DIR, CSV_FILES["users"])
#         users_data = pd.read_csv(users_path, encoding="utf-8")  # UTF-8で読み込む
#         session.bulk_insert_mappings(User, users_data.to_dict(orient="records"))

#         # Industriesデータ
#         industries_path = os.path.join(CSV_DIR, CSV_FILES["industries"])
#         industries_data = pd.read_csv(industries_path, encoding="utf-8")  # UTF-8で読み込む
#         session.bulk_insert_mappings(Industry, industries_data.to_dict(orient="records"))

#         # JobTitlesデータ
#         job_titles_path = os.path.join(CSV_DIR, CSV_FILES["job_titles"])
#         job_titles_data = pd.read_csv(job_titles_path, encoding="utf-8")  # UTF-8で読み込む
#         session.bulk_insert_mappings(JobTitle, job_titles_data.to_dict(orient="records"))

#         # Skillsデータ
#         skills_path = os.path.join(CSV_DIR, CSV_FILES["skills"])
#         skills_data = pd.read_csv(skills_path, encoding="utf-8")  # UTF-8で読み込む
#         session.bulk_insert_mappings(Skill, skills_data.to_dict(orient="records"))

#         # Projectsデータ
#         projects_path = os.path.join(CSV_DIR, CSV_FILES["projects"])
#         projects_data = pd.read_csv(projects_path, encoding="utf-8")  # UTF-8で読み込む
#         session.bulk_insert_mappings(Project, projects_data.to_dict(orient="records"))

#         # コミット
#         session.commit()
#         print("All data inserted successfully from CSV files.")
    
#     except Exception as e:
#         session.rollback()
#         print("Error occurred while inserting data:", e)
#     finally:
#         session.close()

# if __name__ == "__main__":
#     # 初期化（テーブル作成）
#     init_db()
    
#     # データ挿入
#     insert_data_from_csv()


# UTF-8指定前のコード。こっちの方が分かりやすいが上記を採用
# import os
# import pandas as pd
# from database import init_db, get_session
# from models import Office, User, Industry, JobTitle, Skill, Project

# # テーブルごとのデータ挿入関数
# def insert_data_from_csv(session, model, csv_path):
#     data = pd.read_csv(csv_path)
#     session.bulk_insert_mappings(model, data.to_dict(orient="records"))

# if __name__ == "__main__":
#     # データベース初期化
#     init_db()
#     session = get_session()

#     # CSVファイルのパス
#     csv_files = {
#         "offices": "csv/offices.csv",
#         "users": "csv/users.csv",
#         "industries": "csv/industries.csv",
#         "job_titles": "csv/job_titles.csv",
#         "skills": "csv/skills.csv",
#         "projects": "csv/projects.csv",
#     }

#     # 各テーブルにデータ挿入
#     insert_data_from_csv(session, Office, csv_files["offices"])
#     insert_data_from_csv(session, User, csv_files["users"])
#     insert_data_from_csv(session, Industry, csv_files["industries"])
#     insert_data_from_csv(session, JobTitle, csv_files["job_titles"])
#     insert_data_from_csv(session, Skill, csv_files["skills"])
#     insert_data_from_csv(session, Project, csv_files["projects"])

#     session.commit()
#     session.close()
