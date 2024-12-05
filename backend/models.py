# models.py
# SQLAlchemyを使ってデータベースモデルを定義

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# ベースクラス
Base = declarative_base()

# Officesテーブル
class Office(Base):
    __tablename__ = 'offices'
    office_id = Column(Integer, primary_key=True, autoincrement=True)
    office_name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    area = Column(String(100), nullable=True)
    access = Column(String(255), nullable=True)
    capacity = Column(Integer, nullable=True)
    tags = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Usersとのリレーション
    users = relationship("User", back_populates="office")

# Usersテーブル
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)  # 修正: カラム名を統一
    user_type = Column(String(50), nullable=True)
    office_id = Column(Integer, ForeignKey('offices.office_id'), nullable=True)
    job_id = Column(Integer, ForeignKey('job_titles.job_id'), nullable=True)
    industry_id = Column(Integer, ForeignKey('industries.industry_id'), nullable=True)

    # 他テーブルとのリレーション
    office = relationship("Office", back_populates="users")
    job = relationship("JobTitle", back_populates="users")
    industry = relationship("Industry", back_populates="users")
    skills = relationship("Skill", back_populates="user")
    projects = relationship("Project", back_populates="user")

# Industriesテーブル
class Industry(Base):
    __tablename__ = 'industries'
    industry_id = Column(Integer, primary_key=True, autoincrement=True)
    industry_name = Column(String(100), nullable=False)

    # Usersとのリレーション
    users = relationship("User", back_populates="industry")

# JobTitlesテーブル
class JobTitle(Base):
    __tablename__ = 'job_titles'
    job_id = Column(Integer, primary_key=True, autoincrement=True)
    job_title = Column(String(100), nullable=False)

    # Usersとのリレーション
    users = relationship("User", back_populates="job")

# Skillsテーブル
class Skill(Base):
    __tablename__ = 'skills'
    skill_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    skill_name = Column(String(100), nullable=False)
    skill_description = Column(Text, nullable=True)

    # Usersとのリレーション
    user = relationship("User", back_populates="skills")

# Projectsテーブル
class Project(Base):
    __tablename__ = 'projects'
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    project_name = Column(String(100), nullable=False)
    project_description = Column(Text, nullable=True)

    # Usersとのリレーション
    user = relationship("User", back_populates="projects")
