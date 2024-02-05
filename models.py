from sqlalchemy import (Column, Integer, String, Float, ForeignKey)
from sqlalchemy.orm import relationship
from base import Base

class Act_User(Base):
    __tablename__ = 'act_user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_user = Column(String(124), nullable=False)
    id_papers = Column(Integer, nullable=True)

class Paper(Base):
    __tablename__ = 'paper'
    paper_id = Column(Integer, primary_key=True, autoincrement=True)
    name_paper = Column(String(60))
    last_price = Column(Float, nullable=True)

class User_Papers(Base):
    __tablename__ = 'user_papers'
    third_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('act_user.user_id'))
    paper_id = Column(Integer, ForeignKey('paper.paper_id'))
    