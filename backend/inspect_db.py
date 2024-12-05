from sqlalchemy import inspect
from database import engine

def inspect_database():
    # データベースインスペクターを作成
    inspector = inspect(engine)

    # 全テーブルを取得
    tables = inspector.get_table_names()

    print("データベース内のテーブルと制約情報:\n")

    for table in tables:
        print(f"Table: {table}")

        # Primary Keyの確認
        pk = inspector.get_pk_constraint(table)
        print(f"  Primary Key: {pk['constrained_columns']}")

        # Foreign Keyの確認
        fks = inspector.get_foreign_keys(table)
        if fks:
            for fk in fks:
                print(f"  Foreign Key: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        else:
            print("  Foreign Key: None")

        # カラム情報の表示
        columns = inspector.get_columns(table)
        print("  Columns:")
        for column in columns:
            print(f"    - {column['name']} ({column['type']})")

    print("\n検証が完了しました。")

if __name__ == "__main__":
    inspect_database()
