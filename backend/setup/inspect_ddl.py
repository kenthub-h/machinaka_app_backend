from database import Base, engine
import models  # 必要なモデルをインポート

# テーブルのDDL（データ定義SQL）を確認
def inspect_ddl():
    with engine.connect() as conn:
        for table_name in Base.metadata.tables:
            print(f"--- DDL for table '{table_name}' ---")
            try:
                ddl_statement = str(
                    Base.metadata.tables[table_name]
                    .to_metadata(Base.metadata)
                    .create(bind=engine, checkfirst=False)
                    .compile(engine, compile_kwargs={"literal_binds": True})
                )
                print(ddl_statement)
            except Exception as e:
                print(f"Error generating DDL for table '{table_name}': {e}")

if __name__ == "__main__":
    inspect_ddl()
