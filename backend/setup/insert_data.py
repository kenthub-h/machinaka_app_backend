#insert_data.py
from database import init_db, get_session
from models import Office, User, Industry, JobTitle

def insert_initial_data():
    session = get_session()

    # Industriesデータ
    industries = [
        Industry(industry_id=1, industry_name="IT・ソフトウェア"),
        Industry(industry_id=2, industry_name="製造業"),
        Industry(industry_id=3, industry_name="医療・ヘルスケア"),
        Industry(industry_id=4, industry_name="教育・研修"),
        Industry(industry_id=5, industry_name="金融・保険"),
        Industry(industry_id=6, industry_name="不動産・建築"),
        Industry(industry_id=7, industry_name="エンターテインメント"),
        Industry(industry_id=8, industry_name="観光・旅行"),
        Industry(industry_id=9, industry_name="エネルギー・環境"),
        Industry(industry_id=10, industry_name="小売・卸売"),
    ]
    session.add_all(industries)

    # Jobsデータ
    jobs = [
        JobTitle(job_id=1, job_title="ソフトウェアエンジニア"),
        JobTitle(job_id=2, job_title="プロジェクトマネージャー"),
        JobTitle(job_id=3, job_title="データサイエンティスト"),
        JobTitle(job_id=4, job_title="UX/UIデザイナー"),
        JobTitle(job_id=5, job_title="営業マネージャー"),
        JobTitle(job_id=6, job_title="カスタマーサポートスペシャリスト"),
        JobTitle(job_id=7, job_title="人事コーディネーター"),
        JobTitle(job_id=8, job_title="マーケティングアナリスト"),
        JobTitle(job_id=9, job_title="ITセキュリティアナリスト"),
        JobTitle(job_id=10, job_title="プロダクトオーナー"),
    ]
    session.add_all(jobs)

    # Officesデータ
    offices = [
        Office(office_id=1, office_name="中目黒オフィス", address="東京都目黒区中目黒1-1-1", area="東京", access="中目黒駅徒歩2分", capacity=20, tags="駅近, 都内, 人気エリア", latitude=35.644022, longitude=139.698593),
        Office(office_id=2, office_name="三軒茶屋オフィス", address="東京都世田谷区三軒茶屋2-2-2", area="東京", access="三軒茶屋駅徒歩3分", capacity=15, tags="アクセス良好, 静かな環境", latitude=35.641274, longitude=139.669925),
        # ここに残りのオフィスデータを追加してください
    ]
    session.add_all(offices)

    # Usersデータ
    users = [
        User(user_id=1, name="街中太郎", user_type="Owner", office_id=1, job_id=1, industry_id=1),
        User(user_id=2, name="街中次郎", user_type="Owner", office_id=2, job_id=2, industry_id=2),
        User(user_id=3, name="町中一郎", user_type="Expert", office_id=3, job_id=3, industry_id=3),
        User(user_id=4, name="町中二郎", user_type="Expert", office_id=4, job_id=4, industry_id=4),
        User(user_id=5, name="町中三郎", user_type="Expert", office_id=5, job_id=5, industry_id=5),
    ]
    session.add_all(users)

    # コミットしてデータを保存
    session.commit()
    session.close()

if __name__ == "__main__":
    init_db()  # テーブル作成
    insert_initial_data()  # データ挿入
